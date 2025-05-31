import os

import requests
from django.core.cache import cache

AUTH = ("jerit-baiju", os.environ["github_api"])


def fetch_stars(repo_name):
    """
    Fetch the number of stars for a given GitHub repository.
    Results are cached for 24 hours to reduce API calls.

    Args:
        repo_name (str): The name of the repository in the format 'owner/repo'.

    Returns:
        int: The number of stars for the repository, or 0 if the repository does not exist.
    """
    # Create a unique cache key for this repo and metric
    cache_key = f"github_stars_{repo_name}"

    # Try to get cached value first
    cached_value = cache.get(cache_key)
    if cached_value is not None:
        return cached_value

    # If not in cache, fetch from GitHub API
    try:
        url = f"https://api.github.com/repos/{repo_name}"
        response = requests.get(url, timeout=10, auth=AUTH)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        stars_count = data.get("stargazers_count", 0)

        # Cache the result for 24 hours (86400 seconds)
        cache.set(cache_key, stars_count, timeout=86400)

        return stars_count
    except requests.RequestException:
        return 0


def fetch_forks(repo_name):
    """
    Fetch the number of forks for a given GitHub repository.
    Results are cached for 24 hours to reduce API calls.

    Args:
        repo_name (str): The name of the repository in the format 'owner/repo'.

    Returns:
        int: The number of forks for the repository, or 0 if the repository does not exist.
    """
    # Create a unique cache key for this repo and metric
    cache_key = f"github_forks_{repo_name}"

    # Try to get cached value first
    cached_value = cache.get(cache_key)
    if cached_value is not None:
        return cached_value

    # If not in cache, fetch from GitHub API
    try:
        url = f"https://api.github.com/repos/{repo_name}"
        response = requests.get(url, timeout=10, auth=AUTH)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()
        forks_count = data.get("forks_count", 0)

        # Cache the result for 24 hours (86400 seconds)
        cache.set(cache_key, forks_count, timeout=86400)

        return forks_count
    except requests.RequestException:
        return 0
