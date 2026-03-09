#!/usr/bin/env python3
"""
소셜 공유 버튼을 모든 게시글 하단에 추가하는 스크립트.
CSS-only 경량 방식 (외부 JS/플러그인 불필요).
engine.py의 cookie auth 방식 사용.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from engine import login, REST

SOCIAL_SHARE_BLOCK = '''
<!-- wp:html -->
<style>
.social-share-bar{display:flex;gap:10px;flex-wrap:wrap;margin:2em 0 1em;padding:1.2em 0;border-top:2px solid #e0e0e0}
.social-share-bar a{display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:6px;color:#fff;text-decoration:none;font-size:14px;font-weight:600;transition:opacity .2s}
.social-share-bar a:hover{opacity:.85}
.social-share-bar .share-label{color:#555;font-weight:700;font-size:14px;align-self:center}
.ss-x{background:#000}.ss-fb{background:#1877f2}.ss-li{background:#0a66c2}.ss-rd{background:#ff4500}.ss-pin{background:#e60023}.ss-email{background:#555}
@media(max-width:600px){.social-share-bar{gap:8px}.social-share-bar a{padding:8px 12px;font-size:13px}}
</style>
<div class="social-share-bar">
  <span class="share-label">Share:</span>
  <a class="ss-x" href="https://twitter.com/intent/tweet?url=PERMALINK&text=TITLE" target="_blank" rel="noopener">𝕏 Post</a>
  <a class="ss-fb" href="https://www.facebook.com/sharer/sharer.php?u=PERMALINK" target="_blank" rel="noopener">Facebook</a>
  <a class="ss-li" href="https://www.linkedin.com/sharing/share-offsite/?url=PERMALINK" target="_blank" rel="noopener">LinkedIn</a>
  <a class="ss-rd" href="https://reddit.com/submit?url=PERMALINK&title=TITLE" target="_blank" rel="noopener">Reddit</a>
  <a class="ss-pin" href="https://pinterest.com/pin/create/button/?url=PERMALINK&description=TITLE" target="_blank" rel="noopener">Pinterest</a>
  <a class="ss-email" href="mailto:?subject=TITLE&body=Check%20this%20out:%20PERMALINK" rel="noopener">Email</a>
</div>
<!-- /wp:html -->
'''

def add_share_buttons():
    s, h = login()

    # 모든 게시글 가져오기
    page = 1
    all_posts = []
    while True:
        resp = s.get(f"{REST}/posts?per_page=50&page={page}&_fields=id,title,link,content", headers=h)
        if resp.status_code != 200:
            break
        posts = resp.json()
        if not posts:
            break
        all_posts.extend(posts)
        page += 1

    print(f"총 {len(all_posts)}개 게시글 발견\n")

    updated = 0
    skipped = 0
    for post in all_posts:
        pid = post['id']
        title = post['title']['rendered']
        link = post['link']
        content = post['content']['rendered']

        # 이미 소셜 공유 버튼이 있는지 확인
        if 'social-share-bar' in content:
            print(f"  ⏭ [{pid}] {title[:50]} — 이미 있음")
            skipped += 1
            continue

        # 원본 content (raw) 가져오기
        raw_resp = s.get(f"{REST}/posts/{pid}?context=edit&_fields=content", headers=h)
        if raw_resp.status_code != 200:
            print(f"  ❌ [{pid}] raw content 가져오기 실패: {raw_resp.status_code}")
            continue
        raw_content = raw_resp.json()['content']['raw']

        # URL 인코딩된 퍼머링크와 제목으로 공유 블록 생성
        import urllib.parse
        encoded_url = urllib.parse.quote(link, safe='')
        encoded_title = urllib.parse.quote(title, safe='')
        share_block = SOCIAL_SHARE_BLOCK.replace('PERMALINK', encoded_url).replace('TITLE', encoded_title)

        # 글 끝에 공유 버튼 추가
        new_content = raw_content + "\n" + share_block

        # 업데이트
        resp = s.post(f"{REST}/posts/{pid}", headers=h, json={"content": new_content})
        if resp.status_code == 200:
            print(f"  ✅ [{pid}] {title[:50]}")
            updated += 1
        else:
            print(f"  ❌ [{pid}] 업데이트 실패: {resp.status_code} {resp.text[:100]}")

    print(f"\n완료: {updated}개 업데이트, {skipped}개 스킵 (이미 있음)")

if __name__ == "__main__":
    add_share_buttons()
