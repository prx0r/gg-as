"""GitHub GraphQL client — 5-10x more efficient than REST for graph traversal."""

from __future__ import annotations

import os
from typing import Any

from gitgoblin.http_client import ResilientHTTP


GRAPHQL_URL = "https://api.github.com/graphql"


class GitHubGraphQL:
    """GraphQL client for efficient graph traversal."""
    
    def __init__(self, token: str):
        self.token = token
        self.client = httpx.Client(
            base_url="https://api.github.com",
            headers={
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            },
            timeout=30.0,
        )
        self.points_used = 0
        self.points_limit = 5000
    
    def query(self, query: str, variables: dict = None) -> dict:
        """Execute a GraphQL query."""
        payload = {"query": query}
        if variables:
            payload["variables"] = variables
        
        resp = self.client.post("/graphql", json=payload)
        resp.raise_for_status()
        
        # Track points (each query costs points based on complexity)
        # Rough estimate: each field costs ~1 point
        self.points_used += 100  # Conservative estimate
        
        return resp.json()
    
    def get_repo_with_stargazers(self, owner: str, name: str, stargazer_limit: int = 10) -> dict:
        """Get repo + stargazers in ONE call (would be 2+ REST calls)."""
        query = """
        query($owner: String!, $name: String!, $stargazerLimit: Int!) {
            repository(owner: $owner, name: $name) {
                name
                description
                url
                stargazerCount
                forkCount
                createdAt
                updatedAt
                primaryLanguage { name }
                repositoryTopics(first: 10) {
                    nodes { topic { name } }
                }
                stargazers(first: $stargazerLimit) {
                    nodes {
                        login
                        name
                        company
                        bio
                    }
                }
            }
        }
        """
        return self.query(query, {"owner": owner, "name": name, "stargazerLimit": stargazer_limit})
    
    def get_user_repos_and_starred(self, username: str, repo_limit: int = 10, starred_limit: int = 10) -> dict:
        """Get user's repos + their starred repos in ONE call."""
        query = """
        query($username: String!, $repoLimit: Int!, $starredLimit: Int!) {
            user(login: $username) {
                login
                name
                bio
                company
                repositories(first: $repoLimit, orderBy: {field: STARGazers, direction: DESC}) {
                    nodes {
                        name
                        description
                        stargazerCount
                        primaryLanguage { name }
                    }
                }
                starredRepositories(first: $starredLimit) {
                    nodes {
                        nameWithOwner
                        description
                        stargazerCount
                    }
                }
            }
        }
        """
        return self.query(query, {"username": username, "repoLimit": repo_limit, "starredLimit": starred_limit})
    
    def get_repo_contributors(self, owner: str, name: str, contributor_limit: int = 10) -> dict:
        """Get repo contributors with their other repos in ONE call."""
        query = """
        query($owner: String!, $name: String!, $limit: Int!) {
            repository(owner: $owner, name: $name) {
                name
                contributors(first: $limit) {
                    nodes {
                        login
                        name
                        bio
                        repositories(first: 5, orderBy: {field: STARGazers, direction: DESC}) {
                            nodes {
                                nameWithOwner
                                stargazerCount
                            }
                        }
                    }
                }
            }
        }
        """
        return self.query(query, {"owner": owner, "name": name, "limit": contributor_limit})
    
    def get_pr_activity(self, owner: str, name: str, pr_limit: int = 10) -> dict:
        """Get recent PRs with authors and their profiles."""
        query = """
        query($owner: String!, $name: String!, $limit: Int!) {
            repository(owner: $owner, name: $name) {
                pullRequests(first: $limit, orderBy: {field: CREATED_AT, direction: DESC}) {
                    nodes {
                        title
                        createdAt
                        author { login, name, company }
                        additions
                        deletions
                        files(first: 5) {
                            nodes { path }
                        }
                    }
                }
            }
        }
        """
        return self.query(query, {"owner": owner, "name": name, "limit": pr_limit})
    
    def get_issue_activity(self, owner: str, name: str, issue_limit: int = 10) -> dict:
        """Get recent issues with commenters."""
        query = """
        query($owner: String!, $name: String!, $limit: Int!) {
            repository(owner: $owner, name: $name) {
                issues(first: $limit, orderBy: {field: CREATED_AT, direction: DESC}) {
                    nodes {
                        title
                        createdAt
                        author { login }
                        comments(first: 5) {
                            nodes { author { login } }
                        }
                    }
                }
            }
        }
        """
        return self.query(query, {"owner": owner, "name": name, "limit": issue_limit})
    
    def get_dependency_graph(self, owner: str, name: str) -> dict:
        """Get repository dependency graph."""
        query = """
        query($owner: String!, $name: String!) {
            repository(owner: $owner, name: $name) {
                dependencyGraphManifests(first: 5) {
                    nodes {
                        filename
                        dependencies(first: 20) {
                            nodes {
                                packageName
                                packageManager
                            }
                        }
                    }
                }
            }
        }
        """
        return self.query(query, {"owner": owner, "name": name})
    
    def batch_repos(self, repos: list[tuple[str, str]]) -> dict:
        """Batch multiple repo lookups in one query (max ~10 per query)."""
        # GraphQL has a limit on query complexity
        # Split into batches of 5
        results = {}
        
        for i in range(0, len(repos), 5):
            batch = repos[i:i+5]
            
            # Build dynamic query
            parts = []
            for j, (owner, name) in enumerate(batch):
                parts.append(f"""
                repo{j}: repository(owner: "{owner}", name: "{name}") {{
                    nameWithOwner
                    description
                    stargazerCount
                    primaryLanguage {{ name }}
                }}
                """)
            
            query = "{ " + " ".join(parts) + " }"
            result = self.query(query)
            
            if "data" in result:
                for key, repo_data in result["data"].items():
                    if repo_data:
                        results[repo_data.get("nameWithOwner", key)] = repo_data
            
            self.points_used += len(batch) * 50
        
        return results
