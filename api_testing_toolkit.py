import requests
import json

class APIClient:
    """A simple API client — similar to how you'd organize a Postman collection."""
    
    def __init__(self, base_url, headers=None):
        self.base_url = base_url.rstrip("/")
        self.default_headers = headers or {}
    
    def _request(self, method, path, **kwargs):
        """Make a request and return a formatted result."""
        url = f"{self.base_url}{path}"
        
        # Merge default headers with any request-specific headers
        headers = {**self.default_headers, **kwargs.pop("headers", {})}
        
        response = requests.request(method, url, headers=headers, **kwargs)
        
        return {
            "status": response.status_code,
            "reason": response.reason,
            "time_ms": response.elapsed.total_seconds() * 1000,
            "data": response.json() if response.text else None,
            "headers": dict(response.headers),
        }
    
    def get(self, path, **kwargs):
        return self._request("GET", path, **kwargs)
    
    def post(self, path, **kwargs):
        return self._request("POST", path, **kwargs)
    
    def put(self, path, **kwargs):
        return self._request("PUT", path, **kwargs)
    
    def patch(self, path, **kwargs):
        return self._request("PATCH", path, **kwargs)
    
    def delete(self, path, **kwargs):
        return self._request("DELETE", path, **kwargs)




class JSONPlaceholderClient(APIClient):
    def __init__(self):
        super().__init__("https://jsonplaceholder.typicode.com")
    
    def get_user(self, user_id):
        """Get a specific user's profile."""
        return self.get(f"/users/{user_id}")
    
    def get_user_posts(self, user_id):
        """Get all posts by a specific user."""
        return self.get(f"/posts?userId{user_id}")
    
    
    def create_post(self, user_id, title, body):
        """Create a new post for a user."""
        return self.post("/posts", json={
            
                "userId": user_id,
                "title": title,
                "body": body
            
        })
    
    
    def search_posts(self, query):
        """Search posts by title (client-side filtering)."""
        response = self.get("/posts")
        posts = response["data"]

        matches = []

        for post in posts: 
           if query in post["title"]:
               matches.append(post)

        return matches

client = JSONPlaceholderClient()
print("=== GET /users/5 ===")
result = client.get_user(5)
user = result["data"]

print(f"Name: {user['name']}, City: {user['address']['city']}")


print("=== GET user 5's posts ===")

result = client.get_user_posts(5)
posts = result["data"]

print(f"Post count: {len(posts)}")



print("=== CREATE new post ===")

result = client.create_post(
    5,
    "My Test Post",
    "Testing my JSONPlaceholder client"
)

result["data"]["id"]
print(f"New post ID: {result['data']['id']}")


print("=== SEARCH posts ===")

matches = client.search_posts("qui")

print(f"Matching posts: {len(matches)}")