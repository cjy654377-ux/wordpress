#!/usr/bin/env python3
"""WP Statistics 데이터 조회 — 텔레그램 보고용"""
import requests, re, json

SITE = "https://rhythmicaleskimo.com"
USER = "cjy654377@gmail.com"
PASS = "Dkflekd1!!"

def login():
    s = requests.Session()
    s.cookies.set("wordpress_test_cookie", "WP+Cookie+check")
    s.post(f"{SITE}/wp-login.php", data={
        "log": USER, "pwd": PASS, "wp-submit": "Log In",
        "redirect_to": "/wp-admin/", "testcookie": "1"
    }, allow_redirects=True)
    return s

def get_stats():
    s = login()
    overview = s.get(f"{SITE}/wp-admin/admin.php?page=wps_overview_page").text

    # WP Statistics 카운트 값 추출 (overview 페이지의 숫자들)
    # 패턴: data-*="숫자" 또는 class에 count 포함
    counts = re.findall(r'class="[^"]*wps-postbox-chart__count[^"]*"[^>]*>[\s]*(\d+)', overview)

    # fallback: 모든 숫자 카운트
    if not counts:
        counts = re.findall(r'>(\d+)</', overview)

    # 오늘/어제/이번주/이번달/총합 패턴 찾기
    today = re.findall(r'(?:today|오늘)[^<]*?(\d+)', overview, re.I)
    yesterday = re.findall(r'(?:yesterday|어제)[^<]*?(\d+)', overview, re.I)

    # WP Statistics overview에서 직접 위젯 데이터 추출
    # data-wps-metric 패턴
    metrics = re.findall(r'data-wps-metric="([^"]+)"[^>]*data-wps-value="([^"]+)"', overview)

    # 게시물 총 수 (WP REST API)
    nonce_m = re.search(r'"nonce":"([a-f0-9]+)"',
                        s.get(f"{SITE}/wp-admin/post-new.php").text)
    total_posts = 0
    if nonce_m:
        h = {"X-WP-Nonce": nonce_m.group(1)}
        r = s.get(f"{SITE}/wp-json/wp/v2/posts?per_page=1&status=publish", headers=h)
        total_posts = int(r.headers.get("X-WP-Total", 0))

        # 카테고리별 게시물 수
        cats = s.get(f"{SITE}/wp-json/wp/v2/categories?per_page=20", headers=h).json()
        cat_stats = []
        for c in cats:
            if c.get("count", 0) > 0:
                cat_stats.append(f"  • {c['name']}: {c['count']}개")

    # WP Statistics DB에서 직접 가져오기 (admin overview 파싱)
    # 방문자/조회수 섹션 파싱
    visitor_section = re.findall(
        r'class="wps-key__title"[^>]*>([^<]+)</span>\s*<span[^>]*>(\d+)</span>',
        overview, re.DOTALL
    )

    # 최종 리포트 구성
    report = []
    report.append(f"📊 사이트 현황 리포트")
    report.append(f"━━━━━━━━━━━━━━━")
    report.append(f"📝 총 게시물: {total_posts}개")

    if cat_stats:
        report.append(f"\n📂 카테고리별:")
        report.extend(cat_stats)

    if visitor_section:
        report.append(f"\n👥 방문 통계:")
        for label, val in visitor_section:
            report.append(f"  • {label.strip()}: {val}")
    elif metrics:
        report.append(f"\n👥 방문 통계:")
        for metric, value in metrics:
            report.append(f"  • {metric}: {value}")
    else:
        # 기본 카운트 (WP Statistics overview의 순서: 오늘방문자, 오늘조회, 어제방문자, 어제조회 등)
        labels = ["오늘 방문자", "오늘 조회수", "어제 방문자", "어제 조회수",
                  "이번주 방문자", "이번주 조회수", "이번달 방문자", "이번달 조회수",
                  "총 방문자", "총 조회수", "어제 검색엔진", "총 검색엔진"]
        if counts and len(counts) >= 2:
            report.append(f"\n👥 방문 통계:")
            for i, c in enumerate(counts[:len(labels)]):
                if i < len(labels):
                    report.append(f"  • {labels[i]}: {c}")

    return "\n".join(report)

if __name__ == "__main__":
    print(get_stats())
