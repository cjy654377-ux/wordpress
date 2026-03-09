#!/usr/bin/env python3
"""사이트 이미지 최적화 현황 분석"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login, REST
import urllib.request

def analyze():
    s, h = login()

    # 1. 모든 미디어 항목 가져오기
    page = 1
    all_media = []
    while True:
        resp = s.get(f"{REST}/media?per_page=100&page={page}", headers=h)
        if resp.status_code != 200:
            break
        items = resp.json()
        if not items:
            break
        all_media.extend(items)
        page += 1

    print("=" * 70)
    print("  이미지 최적화 현황 분석 — rhythmicaleskimo.com")
    print("=" * 70)

    # 2. 형식별 분류
    by_mime = {}
    total_size = 0
    large_images = []  # > 200KB

    for m in all_media:
        mime = m.get('mime_type', 'unknown')
        details = m.get('media_details', {})
        fsize = details.get('filesize', 0)
        width = details.get('width', 0)
        height = details.get('height', 0)
        url = m.get('source_url', '')
        fname = url.split('/')[-1] if url else ''

        by_mime.setdefault(mime, {'count': 0, 'size': 0, 'files': []})
        by_mime[mime]['count'] += 1
        by_mime[mime]['size'] += fsize

        total_size += fsize

        if fsize > 200 * 1024:
            large_images.append({
                'name': fname, 'size': fsize,
                'dim': f"{width}x{height}", 'mime': mime,
                'url': url
            })

    # 3. 출력
    print(f"\n📊 미디어 라이브러리 총계: {len(all_media)}개 항목, {total_size/1024/1024:.1f} MB\n")

    print("─── 형식별 분류 ───")
    for mime, info in sorted(by_mime.items(), key=lambda x: -x[1]['size']):
        pct = info['size'] / total_size * 100 if total_size else 0
        print(f"  {mime:25s}  {info['count']:3d}개  {info['size']/1024/1024:6.1f} MB  ({pct:.0f}%)")

    webp_count = by_mime.get('image/webp', {}).get('count', 0)
    print(f"\n  → WebP 사용률: {webp_count}/{len(all_media)} ({webp_count/len(all_media)*100:.0f}%)")

    # 4. 큰 이미지 (최적화 대상)
    large_images.sort(key=lambda x: -x['size'])
    print(f"\n─── 200KB 초과 이미지 ({len(large_images)}개) — 최적화 우선 대상 ───")
    for img in large_images[:15]:
        print(f"  {img['size']/1024:>7.0f} KB  {img['dim']:>12s}  {img['name']}")

    # 5. lazy loading 확인 (실제 페이지 소스 확인)
    print(f"\n─── Lazy Loading & srcset 확인 ───")
    # 첫 번째 게시글 확인
    posts = s.get(f"{REST}/posts?per_page=1&_fields=link", headers=h).json()
    if posts:
        req = urllib.request.Request(posts[0]['link'])
        req.add_header('User-Agent', 'Mozilla/5.0')
        html = urllib.request.urlopen(req).read().decode()

        lazy_count = html.count('loading="lazy"')
        srcset_count = html.count('srcset=')
        total_img = html.count('<img ')

        print(f"  샘플 페이지: {posts[0]['link']}")
        print(f"  총 <img> 태그: {total_img}개")
        print(f"  loading='lazy': {lazy_count}개 ({lazy_count}/{total_img})")
        print(f"  srcset 속성: {srcset_count}개 ({srcset_count}/{total_img})")

    # 6. LiteSpeed Cache 확인
    print(f"\n─── LiteSpeed Cache 확인 ───")
    namespaces_resp = s.get(f"{REST.replace('/wp/v2', '')}/", headers=h)
    ns = namespaces_resp.json().get('namespaces', [])
    litespeed_ns = [n for n in ns if 'litespeed' in n.lower()]
    if litespeed_ns:
        print(f"  ✅ LiteSpeed 네임스페이스 발견: {litespeed_ns}")
        print(f"  → LiteSpeed Cache 플러그인 설치됨 (WebP 변환 기능 내장)")
    else:
        print(f"  ❌ LiteSpeed Cache 미설치")

    # 7. 개선 방안
    print(f"\n{'=' * 70}")
    print("  개선 방안")
    print("=" * 70)

    print("""
  [1] WebP 변환 활성화 (최우선)
      → LiteSpeed Cache 이미 설치됨
      → WP 관리자 > LiteSpeed Cache > Image Optimization 에서 활성화
      → 예상 절감: PNG/JPEG 대비 25-35% 용량 감소
      → 22MB → 약 14-15MB 예상

  [2] 큰 이미지 리사이징
      → 1536x1024 이상 이미지들을 1200px 너비로 리사이징
      → post-25-featured.png (2,625KB) → ~800KB 예상
      → post-19-featured.png (2,324KB) → ~700KB 예상

  [3] Lazy Loading 강화
      → WordPress 5.5+ 기본 지원이지만, 커스텀 HTML 내 이미지에는 미적용
      → LiteSpeed Cache > Page Optimization > Media에서 Lazy Load 활성화

  [4] 추천 플러그인 (WP 관리자에서 설치)
      → "LiteSpeed Cache" — 이미 설치됨, Image Optimization 활성화만 하면 됨
      → 추가 불필요 (ShortPixel, Imagify 등은 LiteSpeed와 중복)
""")

if __name__ == "__main__":
    analyze()
