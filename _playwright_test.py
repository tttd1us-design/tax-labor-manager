#!/usr/bin/env python
# Comprehensive browser verification for tax-labor-manager
# Tests: console errors, 5 features, screenshots, DOM capture
import json, os, sys, datetime, re

from playwright.sync_api import sync_playwright

OUT = r"C:\AI_산출물\테스트\tax-labor-manager\검증_20261013"
os.makedirs(OUT, exist_ok=True)

URL = "http://127.0.0.1:8099/index.html"
results = {}
console_errors = []
console_logs = []

def save(name, content):
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-gpu"])
    page = browser.new_page()

    # Capture console messages
    page.on("console", lambda msg: (
        console_errors.append(f"[console {msg.type}] {msg.text}") if msg.type == "error"
        else console_logs.append(f"[console {msg.type}] {msg.text}")
    ))
    page.on("pageerror", lambda exc: console_errors.append(f"[pageerror] {exc}"))

    # Load page
    resp = page.goto(URL, wait_until="networkidle")
    page.wait_for_timeout(1000)  # let render complete

    # Screenshot full page
    shot_path = os.path.join(OUT, "screenshot_fullpage.png")
    page.screenshot(path=shot_path, full_page=True)
    results["screenshot"] = shot_path

    # Save DOM snapshot
    dom = page.content()
    save("dom_snapshot.html", dom)

    # ── TEST 1: Schedule list rendered ──
    items = page.query_selector_all("#schedule-list .schedule-item")
    results["schedule_count"] = len(items)
    results["schedule_texts"] = [page.inner_text(f"#schedule-list .schedule-item:nth-child({i+1})") for i in range(len(items))]

    # ── TEST 2: VAT calculator ──
    # Default values: supply=50,000,000, purchase=3,000,000
    page.evaluate("document.getElementById('vat-supply').value = '50000000'")
    page.evaluate("document.getElementById('vat-purchase').value = '3000000'")
    page.click("#calc-vat")
    page.wait_for_timeout(500)
    vat_result = page.inner_text("#vat-result")
    results["vat_result"] = vat_result

    # ── TEST 3: Income tax calculator ──
    # Default values: income=80,000,000, expense=50,000,000, deduct=1,500,000
    page.evaluate("document.getElementById('income-annual').value = '80000000'")
    page.evaluate("document.getElementById('income-expense').value = '50000000'")
    page.evaluate("document.getElementById('income-deduct').value = '1500000'")
    page.click("#calc-income")
    page.wait_for_timeout(500)
    income_result = page.inner_text("#income-result")
    results["income_result"] = income_result

    # ── TEST 4: Filter ──
    # Count before filter
    before_count = len(page.query_selector_all("#schedule-list .schedule-item"))
    # Search for something specific that will reduce the list
    page.fill("#search-input", "부가세")
    page.click("#search-btn")
    page.wait_for_timeout(500)
    after_count = len(page.query_selector_all("#schedule-list .schedule-item"))
    results["filter_before"] = before_count
    results["filter_after"] = after_count
    results["filter_texts"] = [page.inner_text(f"#schedule-list .schedule-item:nth-child({i+1})") for i in range(after_count)]
    # Clear filter
    page.fill("#search-input", "")
    page.click("#search-btn")
    page.wait_for_timeout(500)

    # ── TEST 5: Disclaimer at top and bottom ──
    # Check for banner/footer elements
    banner_html = page.inner_html("body")
    # Look for disclaimer text patterns
    disclaimer_pattern = re.findall(r'(면책|책임|free\s*language|본\s*서비스|보장|법적인\s*조언|최대한\s*노려|decide|advice)', banner_html, re.IGNORECASE)
    results["disclaimer_matches"] = len(disclaimer_pattern)
    # Check for top_banner and footer classes
    has_top = len(page.query_selector_all(".top_banner")) > 0
    has_footer = len(page.query_selector_all(".footer")) > 0
    results["has_top_banner"] = has_top
    results["has_footer"] = has_footer

    # Check banner text content
    banners = page.query_selector_all(".top_banner")
    footers = page.query_selector_all(".footer")
    results["top_banner_text"] = [page.inner_text(f".top_banner:nth-child({i+1})") for i in range(len(banners))]
    results["foot_banner_text"] = [page.inner_text(f".footer:nth-child({i+1})") for i in range(len(footers))]

    # ── Upcoming count badge ──
    badge_text = page.inner_text("#upcoming-count")
    results["badge_text"] = badge_text

    browser.close()

# Save results
save("test_results.json", json.dumps(results, ensure_ascii=False, indent=2))
save("console_errors.txt", "\n".join(console_errors) if console_errors else "NO CONSOLE ERRORS")
save("console_logs.txt", "\n".join(console_logs) if console_logs else "NO CONSOLE LOGS")

print(json.dumps(results, ensure_ascii=False, indent=2))
print("\n=== CONSOLE ERRORS ===")
print("\n".join(console_errors) if console_errors else "NO CONSOLE ERRORS")
print(f"\nTotal console errors: {len(console_errors)}")
print(f"Total schedule items: {results['schedule_count']}")
print(f"VAT result: {results['vat_result']}")
print(f"Income result: {results['income_result']}")
print(f"Filter: {results['filter_before']} -> {results['filter_after']}")
