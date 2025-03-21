from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup
import cv2
import numpy as np
import whois

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_webpage_content(url):
    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.get_text()
    except Exception:
        return None

def compare_images(img1_path, img2_path):
    try:
        img1 = cv2.imread(img1_path, cv2.IMREAD_GRAYSCALE)
        img2 = cv2.imread(img2_path, cv2.IMREAD_GRAYSCALE)
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        similarity = len(matches) / max(len(kp1), len(kp2))
        return similarity
    except Exception:
        return 0.0

def predict_phishing(domain, genuine_url):
    try:
        domain_info = whois.whois(domain)
        domain_content = get_webpage_content(f"http://{domain}")
        genuine_content = get_webpage_content(f"http://{genuine_url}")
        content_similarity = 0.5  # Placeholder
        img_similarity = 0.3  # Placeholder
        score = (content_similarity + img_similarity) / 2
        return {"domain": domain, "score": score, "is_phishing": score > 0.7}
    except Exception as e:
        return {"domain": domain, "score": 0.0, "is_phishing": False, "error": str(e)}

@app.post("/analyze")
async def analyze_domain(data: dict):
    domain = data.get("domain")
    genuine_url = data.get("genuine_url", "example.com")
    result = predict_phishing(domain, genuine_url)
    return result