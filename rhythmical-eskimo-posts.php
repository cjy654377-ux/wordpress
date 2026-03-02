<?php
/**
 * Plugin Name: Rhythmical Eskimo - Auto Posts
 * Plugin URI:  https://rhythmicaleskimo.com
 * Description: Automatically publishes 10 생생정보통 blog posts upon activation.
 * Version:     1.0.0
 * Author:      Rhythmical Eskimo
 * Author URI:  https://rhythmicaleskimo.com
 * License:     GPL-2.0-or-later
 * License URI: https://www.gnu.org/licenses/gpl-2.0.html
 * Text Domain: rhythmical-eskimo-posts
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit; // Prevent direct access.
}

// ---------------------------------------------------------------------------
// Activation hook
// ---------------------------------------------------------------------------
register_activation_hook( __FILE__, 'rep_activate' );

function rep_activate() {
    rep_create_posts();
    set_transient( 'rep_activation_notice', true, 60 );
}

// ---------------------------------------------------------------------------
// Deactivation hook — posts are intentionally kept
// ---------------------------------------------------------------------------
register_deactivation_hook( __FILE__, 'rep_deactivate' );

function rep_deactivate() {
    // No-op: posts remain published after plugin deactivation.
}

// ---------------------------------------------------------------------------
// Admin notice
// ---------------------------------------------------------------------------
add_action( 'admin_notices', 'rep_admin_notice' );

function rep_admin_notice() {
    if ( get_transient( 'rep_activation_notice' ) ) {
        delete_transient( 'rep_activation_notice' );
        echo '<div class="notice notice-success is-dismissible">'
           . '<p><strong>10개 생생정보통 게시물이 발행되었습니다!</strong></p>'
           . '</div>';
    }
}

// ---------------------------------------------------------------------------
// Helper: get or create the '생생정보통' category
// ---------------------------------------------------------------------------
function rep_get_or_create_category() {
    $cat_name = '생생정보통';
    $term     = term_exists( $cat_name, 'category' );

    if ( ! $term ) {
        $term = wp_insert_term( $cat_name, 'category' );
    }

    if ( is_wp_error( $term ) ) {
        return 1; // Fall back to the default "Uncategorized" category.
    }

    return (int) ( is_array( $term ) ? $term['term_id'] : $term );
}

// ---------------------------------------------------------------------------
// Helper: parse tags from <span class="tag">#...</span> markup
// ---------------------------------------------------------------------------
function rep_extract_tags( $html ) {
    $tags = array();

    if ( preg_match_all( '/<span[^>]+class=["\']tag["\'][^>]*>(.*?)<\/span>/i', $html, $matches ) ) {
        foreach ( $matches[1] as $raw ) {
            // Strip the leading # and any HTML entities / whitespace.
            $tag = trim( wp_strip_all_tags( html_entity_decode( $raw, ENT_QUOTES, 'UTF-8' ) ) );
            $tag = ltrim( $tag, '#' );
            if ( $tag !== '' ) {
                $tags[] = $tag;
            }
        }
    }

    return array_unique( $tags );
}

// ---------------------------------------------------------------------------
// Main: create all 10 posts
// ---------------------------------------------------------------------------
function rep_create_posts() {
    $category_id = rep_get_or_create_category();

    $posts_data = rep_get_posts_data();

    foreach ( $posts_data as $data ) {

        // Skip if a post with this exact title already exists.
        $existing = get_page_by_title( $data['title'], OBJECT, 'post' );
        if ( $existing ) {
            continue;
        }

        // Build the post content: prepend the <style> block then the body content.
        $post_content = $data['style'] . "\n\n" . $data['body'];

        $post_id = wp_insert_post( array(
            'post_title'   => wp_strip_all_tags( $data['title'] ),
            'post_content' => $post_content,
            'post_status'  => 'publish',
            'post_type'    => 'post',
            'post_category' => array( $category_id ),
        ), true );

        if ( is_wp_error( $post_id ) ) {
            continue;
        }

        // Assign tags.
        if ( ! empty( $data['tags'] ) ) {
            wp_set_post_tags( $post_id, $data['tags'], false );
        }
    }
}

// ---------------------------------------------------------------------------
// Post data — content extracted from each HTML file
// ---------------------------------------------------------------------------
function rep_get_posts_data() {

    // Shared <style> block (identical across all 10 files).
    $common_style = <<<'STYLE'
<style>
.saenginfo-post { font-family: 'Noto Sans KR', sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; line-height: 1.8; color: #333; }
.saenginfo-post h1 { font-size: 24px; color: #d63031; border-bottom: 3px solid #d63031; padding-bottom: 10px; }
.saenginfo-post h2 { font-size: 20px; color: #2d3436; margin-top: 30px; }
.saenginfo-post .meta { color: #636e72; font-size: 14px; margin-bottom: 20px; }
.saenginfo-post .highlight-box { background: #ffeaa7; padding: 15px 20px; border-radius: 10px; margin: 20px 0; }
.saenginfo-post .menu-table { width: 100%; border-collapse: collapse; margin: 15px 0; }
.saenginfo-post .menu-table th,
.saenginfo-post .menu-table td { border: 1px solid #ddd; padding: 10px; text-align: left; }
.saenginfo-post .menu-table th { background: #d63031; color: white; }
.saenginfo-post .info-card { background: #f8f9fa; border-left: 4px solid #d63031; padding: 15px; margin: 20px 0; }
.saenginfo-post .tag { display: inline-block; background: #74b9ff; color: white; padding: 3px 10px; border-radius: 15px; margin: 3px; font-size: 13px; }
.saenginfo-post .image-placeholder { background: #dfe6e9; height: 400px; display: flex; align-items: center; justify-content: center; border-radius: 10px; margin: 20px 0; font-size: 18px; color: #636e72; }
.saenginfo-post .price-badge { background: #e17055; color: white; font-size: 28px; font-weight: bold; padding: 10px 20px; border-radius: 10px; display: inline-block; }
.saenginfo-post .cta { background: #d63031; color: white; padding: 15px; text-align: center; border-radius: 10px; margin: 30px 0; font-size: 18px; }
</style>
STYLE;

    return array(

        // ------------------------------------------------------------------ 01
        array(
            'title' => '[생생정보] 방이굴림만두떼굴 - 밀가루 없는 수제 굴림 만두전골! 서울 송파구 방이동 맛집',
            'style' => $common_style,
            'tags'  => array( '생생정보', '장사의신', '방이굴림만두떼굴', '송파구맛집', '방이동맛집', '굴림만두전골', '만두전골', '올림픽공원맛집', '서울맛집', 'KBS생생정보' ),
            'body'  => <<<'BODY'
<div class="saenginfo-post">

<h1>🍲 [2TV 생생정보] 방이굴림만두떼굴 - 밀가루 없는 수제 굴림 만두전골! 서울 송파구 방이동 숨은 맛집</h1>

<p class="meta">📺 2026년 2월 27일 방송 | KBS2 2TV 생생정보 | 코너: 장사의 신</p>

<img src="images/01_main.jpeg" alt="방이굴림만두떼굴 굴림만두전골" style="width:100%; border-radius:10px; margin:20px 0;">

<p>안녕하세요! 오늘은 <strong>2TV 생생정보 '장사의 신'</strong> 코너에서 소개된 <strong>서울 송파구 방이동</strong>의 숨은 맛집 <strong>방이굴림만두떼굴</strong>을 소개해드리려고 합니다.</p>

<p>올림픽공원 바로 옆, 방이동에 위치한 이 맛집의 시그니처 메뉴는 바로 <strong>"밀가루 없는 수제 굴림 만두전골"</strong>입니다! 🥟</p>

<div class="highlight-box">
💡 <strong>이 맛집이 특별한 이유:</strong> 밀가루 반죽 대신 직접 빚은 수제 만두를 사용하고, 진한 육수와 신선한 채소가 어우러진 건강한 만두전골을 선보입니다.
</div>

<h2>📍 맛집 기본 정보</h2>

<div class="info-card">
<strong>🏪 가게명:</strong> 방이굴림만두떼굴<br>
<strong>🏠 위치:</strong> 서울 송파구 방이동 (올림픽공원 인근)<br>
<strong>🚇 교통:</strong> 방이역 또는 올림픽공원역 하차 후 도보<br>
<strong>📺 방송:</strong> 2TV 생생정보 2026.02.27 '장사의 신' 코너<br>
<strong>🅿️ 주차:</strong> 인근 공영주차장 이용 가능<br>
<strong>📌 특이사항:</strong> KSPO돔(올림픽공원) 방문 시 함께 방문 추천
</div>

<h2>🍽️ 대표 메뉴</h2>

<table class="menu-table">
<tr><th>메뉴</th><th>특징</th></tr>
<tr><td>🥇 굴림만두전골</td><td>밀가루 없는 수제 굴림 만두 + 진한 육수 + 신선한 채소, 시그니처 메뉴</td></tr>
<tr><td>🍚 곤드레죽</td><td>전골 후 마무리로 즐기는 고소한 곤드레죽</td></tr>
</table>

<img src="images/01_menu.jpeg" alt="방이굴림만두떼굴 메뉴" style="width:100%; border-radius:10px; margin:20px 0;">

<h2>💬 실제 방문 후기</h2>

<blockquote style="background:#f1f2f6; padding:15px; border-radius:10px; border-left:4px solid #d63031;">
"육수도 진하고 채소도 신선해요. 밀가루 없는 만두라 속이 편하고 건강한 느낌!"
</blockquote>

<h2>🚗 찾아가는 길</h2>

<p>🚇 <strong>지하철:</strong> 방이역 또는 올림픽공원역 하차 후 도보<br>
🚌 <strong>버스:</strong> 올림픽공원 방면 버스 이용<br>
🅿️ <strong>주차:</strong> 인근 공영주차장 이용</p>

<iframe src="https://map.kakao.com/?urlX=520951&urlY=1110890&name=%EB%B0%A9%EC%9D%B4%EA%B5%B4%EB%A6%BC%EB%A7%8C%EB%91%90%EB%96%BC%EA%B5%B4&map_type=TYPE_MAP&from=roughmap" width="100%" height="350" style="border:none; border-radius:10px; margin:20px 0;"></iframe>
<p style="font-size:13px; color:#999;">📍 서울특별시 송파구 양재대로71길 4-27 (방이동) | ☎ 02-415-5999</p>

<div class="cta">
🔥 올림픽공원 나들이 + 만두전골 맛집 코스로 완벽한 하루!
</div>

<h2>🏷️ 관련 태그</h2>
<span class="tag">#생생정보</span>
<span class="tag">#장사의신</span>
<span class="tag">#방이굴림만두떼굴</span>
<span class="tag">#송파구맛집</span>
<span class="tag">#방이동맛집</span>
<span class="tag">#굴림만두전골</span>
<span class="tag">#만두전골</span>
<span class="tag">#올림픽공원맛집</span>
<span class="tag">#서울맛집</span>
<span class="tag">#KBS생생정보</span>

<p style="margin-top:30px; font-size:13px; color:#999;">※ 본 포스팅은 KBS 2TV 생생정보 방송 내용을 기반으로 작성되었습니다. 방문 전 영업시간과 메뉴를 확인해주세요.</p>

</div>
BODY
        ),

        // ------------------------------------------------------------------ 02
        array(
            'title' => '[생생정보] 월드밥 - 8,000원 한식 뷔페! 광주 서구 화정동 가성비 끝판왕',
            'style' => $common_style,
            'tags'  => array( '생생정보', '한국인의식판', '월드밥', '광주맛집', '한식뷔페', '무한리필', '가성비맛집', '광주서구맛집', '8000원뷔페', '화정동맛집', '금호월드' ),
            'body'  => <<<'BODY'
<div class="saenginfo-post">

<h1>🍱 [2TV 생생정보] 월드밥 - 단돈 8,000원! 광주 서구 화정동 한식 뷔페 가성비 끝판왕</h1>

<p class="meta">📺 2026년 2월 26일 방송 | KBS2 2TV 생생정보 | 코너: 한국인의 식판</p>

<img src="images/02_main.webp" alt="월드밥 한식뷔페" style="width:100%; border-radius:10px; margin:20px 0;">

<p>요즘 외식 물가가 만만치 않죠? 그런데 <strong>8,000원에 푸짐한 한식 뷔페</strong>를 즐길 수 있는 곳이 있다면 믿으시겠어요?</p>

<p>오늘은 <strong>2TV 생생정보 '한국인의 식판'</strong> 코너에서 소개된 광주 서구 화정동의 가성비 한식 뷔페 <strong>월드밥</strong>을 소개합니다!</p>

<div class="highlight-box">
<div class="price-badge">1인 8,000원</div>
<br><br>
💡 <strong>택시 기사님들의 단골 맛집!</strong> 30~40가지 메뉴를 무한리필로 즐길 수 있는 광주 현지인 맛집입니다.
</div>

<h2>📍 맛집 기본 정보</h2>

<div class="info-card">
<strong>🏪 가게명:</strong> 월드밥<br>
<strong>🏠 위치:</strong> 광주 서구 화정동 금호월드 지하 1층<br>
<strong>💰 가격:</strong> 1인 8,000원 (무한리필 한식 뷔페)<br>
<strong>🍽️ 메뉴 수:</strong> 30~40가지 메뉴 무한리필<br>
<strong>📺 방송:</strong> 2TV 생생정보 2026.02.26 '한국인의 식판' 코너<br>
<strong>👥 추천 대상:</strong> 가족 모임, 직장인 점심, 혼밥도 OK
</div>

<h2>🍽️ 뷔페 구성</h2>

<table class="menu-table">
<tr><th>구분</th><th>내용</th><th>가격</th></tr>
<tr><td>한식 뷔페 (무한리필)</td><td>30~40가지 한식 메뉴 — 국, 찌개, 볶음, 구이, 나물, 김치 등</td><td>1인 8,000원</td></tr>
</table>

<img src="images/02_menu.webp" alt="월드밥 메뉴 구성" style="width:100%; border-radius:10px; margin:20px 0;">

<h2>💬 실제 방문 후기</h2>

<blockquote style="background:#f1f2f6; padding:15px; border-radius:10px; border-left:4px solid #d63031;">
"8,000원에 이 정도 가성비! 광주의 모든 뷔페를 가본 건 아니지만 제가 알고 있는 뷔페에 한해서는 여기가 최고입니다."
</blockquote>

<h2>✨ 이 맛집의 포인트</h2>

<ul>
<li>✅ <strong>가격 대비 최고의 가성비</strong> — 8,000원에 30~40가지 한식 무한리필</li>
<li>✅ <strong>현지인 단골 맛집</strong> — 택시 기사님들이 줄 서는 곳</li>
<li>✅ <strong>금호월드 지하 1층 접근 편리</strong> — 화정동 대형 쇼핑센터 내 위치</li>
<li>✅ <strong>저렴하지만 맛은 확실</strong> — 방송에서도 극찬</li>
</ul>

<div class="cta">
🔥 월드밥 - 광주 여행 필수 코스! 8,000원으로 30~40가지 한식 배 터지게 먹자!
</div>

<h2>🏷️ 관련 태그</h2>
<span class="tag">#생생정보</span>
<span class="tag">#한국인의식판</span>
<span class="tag">#월드밥</span>
<span class="tag">#광주맛집</span>
<span class="tag">#한식뷔페</span>
<span class="tag">#무한리필</span>
<span class="tag">#가성비맛집</span>
<span class="tag">#광주서구맛집</span>
<span class="tag">#8000원뷔페</span>
<span class="tag">#화정동맛집</span>
<span class="tag">#금호월드</span>

<p style="margin-top:30px; font-size:13px; color:#999;">※ 본 포스팅은 KBS 2TV 생생정보 방송 내용을 기반으로 작성되었습니다. 방문 전 영업시간과 메뉴를 확인해주세요.</p>

</div>
BODY
        ),

        // ------------------------------------------------------------------ 03
        array(
            'title' => '[생생정보] 야산해촌 본점 - 설운도 추천! 양평 현지인 14년 단골 생대구탕 맛집',
            'style' => $common_style,
            'tags'  => array( '생생정보', '스타밥집', '야산해촌', '설운도맛집', '양평맛집', '생대구맑은탕', '생대구탕', '양평현지인맛집', '경기도맛집', 'KBS생생정보' ),
            'body'  => <<<'BODY'
<div class="saenginfo-post">

<h1>[2TV 생생정보] 야산해촌 본점 - 설운도 추천! 양평 현지인 14년 단골 생대구탕 맛집</h1>

<p class="meta">2026년 2월 25일 방송 | KBS2 2TV 생생정보 | 코너: 스타 밥집 | 추천: 가수 설운도</p>

<img src="images/03_main.webp" alt="야산해촌 본점 생대구맑은탕" style="width:100%; border-radius:10px; margin:20px 0;">

<p>안녕하세요! 오늘은 <strong>2TV 생생정보 '스타 밥집'</strong> 코너에서 <strong>가수 설운도</strong>가 직접 추천한 <strong>경기 양평</strong>의 숨은 맛집 <strong>야산해촌 본점</strong>을 소개해드리려고 합니다.</p>

<p>양평에서 14년째 살고 있는 설운도가 <strong>현지인 단골 맛집</strong>으로 꼽은 이곳! 시그니처 메뉴는 바로 제철 신선한 재료로 끓여낸 <strong>"생대구맑은탕"</strong>입니다.</p>

<div class="highlight-box">
💡 <strong>이 맛집이 특별한 이유:</strong> 양평 생활 14년 차 가수 설운도가 최고로 꼽는 단골집! 매일 들여오는 신선한 제철 재료와 깊고 시원한 국물 맛이 일품입니다.
</div>

<h2>📍 맛집 기본 정보</h2>

<div class="info-card">
<strong>🏪 가게명:</strong> 야산해촌 본점<br>
<strong>🏠 위치:</strong> 경기도 양평<br>
<strong>📺 방송:</strong> 2TV 생생정보 2026.02.25 '스타 밥집' 코너<br>
<strong>⭐ 추천인:</strong> 가수 설운도 (양평 거주 14년 현지인)<br>
<strong>🅿️ 주차:</strong> 자체 주차 가능<br>
<strong>📌 특이사항:</strong> 신선한 제철 재료 사용, 양평 드라이브 코스와 함께 추천
</div>

<h2>대표 메뉴</h2>

<table class="menu-table">
<tr><th>메뉴</th><th>특징</th></tr>
<tr><td>🥇 생대구맑은탕</td><td>신선한 생대구로 끓여낸 맑고 시원한 국물, 대표 시그니처 메뉴</td></tr>
<tr><td>생선조림</td><td>양념이 잘 배어든 매콤달콤한 생선조림</td></tr>
<tr><td>회무침</td><td>싱싱한 회와 아삭한 채소의 새콤달콤 조화</td></tr>
<tr><td>지리탕</td><td>맑고 담백한 국물이 일품인 보양식</td></tr>
<tr><td>오징어 소면</td><td>쫄깃한 오징어와 소면의 시원한 조합</td></tr>
<tr><td>밀면</td><td>부드러운 면발과 깔끔한 육수의 별미</td></tr>
</table>

<img src="images/03_menu.webp" alt="야산해촌 생대구탕 메뉴" style="width:100%; border-radius:10px; margin:20px 0;">

<h2>실제 방문 후기</h2>

<blockquote style="background:#f1f2f6; padding:15px; border-radius:10px; border-left:4px solid #d63031;">
"국물이 정말 시원하고 깊어요. 대구살도 부드럽고 푸짐하게 나와서 양평 올 때마다 꼭 들르는 곳입니다. 설운도 씨가 추천할 만하네요!"
</blockquote>

<h2>찾아가는 길</h2>

<p><strong>자가용:</strong> 서울에서 중부내륙고속도로 또는 6번 국도 이용, 양평 방면<br>
<strong>대중교통:</strong> 경의중앙선 양평역 하차 후 버스 또는 택시 이용<br>
<strong>주차:</strong> 자체 주차 가능</p>

<iframe src="https://map.kakao.com/?q=%EC%95%BC%EC%82%B0%ED%95%B4%EC%B4%8C+%EC%96%91%ED%8F%89&map_type=TYPE_MAP&from=roughmap" width="100%" height="350" style="border:none; border-radius:10px; margin:20px 0;"></iframe>

<div class="cta">
양평 드라이브 + 설운도 추천 생대구탕으로 완벽한 힐링 여행!
</div>

<h2>관련 태그</h2>
<span class="tag">#생생정보</span>
<span class="tag">#스타밥집</span>
<span class="tag">#야산해촌</span>
<span class="tag">#설운도맛집</span>
<span class="tag">#양평맛집</span>
<span class="tag">#생대구맑은탕</span>
<span class="tag">#생대구탕</span>
<span class="tag">#양평현지인맛집</span>
<span class="tag">#경기도맛집</span>
<span class="tag">#KBS생생정보</span>

<p style="margin-top:30px; font-size:13px; color:#999;">※ 본 포스팅은 KBS 2TV 생생정보 방송 내용을 기반으로 작성되었습니다. 방문 전 영업시간과 메뉴를 확인해주세요.</p>

</div>
BODY
        ),

        // ------------------------------------------------------------------ 04
        array(
            'title' => '[생생정보] 대구 이곡동 이색 중식 맛집 - 왕갈비해물돌판짜장! 달서구 성서산업단지역 인근',
            'style' => $common_style,
            'tags'  => array( '생생정보', '결정적한수', '왕갈비해물돌판짜장', '대구맛집', '달서구맛집', '왕갈비짜장', '이색중식', '이곡동맛집', '성서산업단지역맛집', '두툼탕수육', '초당순두부짬뽕', 'KBS생생정보' ),
            'body'  => <<<'BODY'
<div class="saenginfo-post">

<h1>[2TV 생생정보] 준(Jun) - 대구 이곡동 이색 중식 맛집! 왕갈비해물돌판짜장 달서구 성서산업단지역 인근</h1>

<p class="meta">2026년 2월 24일 방송 | KBS2 2TV 생생정보 | 코너: 결정적 한 수</p>

<img src="images/04_main.jpg" alt="준 왕갈비해물돌판짜장" style="width:100%; border-radius:10px; margin:20px 0;">

<p>안녕하세요! 오늘은 <strong>2TV 생생정보 '결정적 한 수'</strong> 코너에서 소개된 <strong>대구 달서구 이곡동</strong>의 이색 중식 맛집을 소개해드리려고 합니다.</p>

<p>성서산업단지역에서 불과 200m 거리에 위치한 이곳! 짜장면 위에 왕갈비와 해물이 올라간다? <strong>"고기의 재발견"</strong>이라는 표현이 어울리는 이곳은 기존 중식의 틀을 깨는 <strong>이색 중식 한 상</strong>을 선보이는 곳입니다!</p>

<div class="highlight-box">
💡 <strong>이 맛집이 특별한 이유:</strong> 고기의 재발견! 뜨거운 돌판 위에 왕갈비와 해물이 어우러진 짜장면, 쫄깃하면서 육즙 가득한 탕수육까지. 기존 중식에서는 볼 수 없었던 이색적인 메뉴 구성이 압권입니다.
</div>

<h2>📍 맛집 기본 정보</h2>

<div class="info-card">
<strong>🏪 가게명:</strong> 준 (Jun)<br>
<strong>🏠 위치:</strong> 대구 달서구 이곡동 (성서산업단지역 인근 200m)<br>
<strong>📺 방송:</strong> 2TV 생생정보 2026.02.24 '결정적 한 수' 코너<br>
<strong>🅿️ 주차:</strong> 자체 주차 가능<br>
<strong>📌 특이사항:</strong> 코스 요리 주문 시 다양한 이색 중식을 한 번에 즐길 수 있음. 코스 요리로 다양한 이색 중식 한 번에 즐기기 추천
</div>

<h2>대표 메뉴</h2>

<table class="menu-table">
<tr><th>메뉴</th><th>특징</th></tr>
<tr><td>🥇 왕갈비 해물 돌판 짜장</td><td>뜨거운 돌판 위 왕갈비 + 해물 + 짜장의 파격 조합, 시그니처 메뉴</td></tr>
<tr><td>왕갈비 해물 짬뽕</td><td>왕갈비의 깊은 육즙과 해물의 시원함이 어우러진 프리미엄 짬뽕</td></tr>
<tr><td>생등심 두툼 탕수육</td><td>두툼하게 썬 생등심을 사용한 겉바속촉 특제 탕수육</td></tr>
<tr><td>어향가지 새우</td><td>바삭한 새우와 부드러운 가지의 중식 정통 요리</td></tr>
<tr><td>몽글몽글 초당순두부 짬뽕</td><td>부드러운 초당순두부가 들어간 독특한 짬뽕</td></tr>
<tr><td>유니짜장면</td><td>고기와 채소가 잘게 다져진 정통 유니짜장</td></tr>
</table>

<img src="images/04_menu.jpg" alt="준 이색중식 메뉴" style="width:100%; border-radius:10px; margin:20px 0;">

<h2>실제 방문 후기</h2>

<blockquote style="background:#f1f2f6; padding:15px; border-radius:10px; border-left:4px solid #d63031;">
"짜장면에 왕갈비라니, 처음엔 반신반의했는데 한 입 먹고 반했어요. 돌판에 나와서 끝까지 뜨겁고, 탕수육도 쫄깃함이 장난 아닙니다!"
</blockquote>

<h2>찾아가는 길</h2>

<p><strong>지하철:</strong> 대구 지하철 2호선 성서산업단지역, 이곡역, 계명대역 하차 후 도보 이용<br>
<strong>버스:</strong> 달서구 이곡동 방면 시내버스 이용<br>
<strong>주차:</strong> 자체 주차장 이용 가능</p>

<iframe src="https://map.kakao.com/?q=%EC%A4%80+%EB%8C%80%EA%B5%AC+%EB%8B%AC%EC%84%9C%EA%B5%AC+%EC%9D%B4%EA%B3%A1%EB%8F%99&map_type=TYPE_MAP&from=roughmap" width="100%" height="350" style="border:none; border-radius:10px; margin:20px 0;"></iframe>
<p style="font-size:13px; color:#999;">📍 대구 달서구 달구벌대로251안길 5-6 | ☎ 0507-1481-7773</p>

<div class="cta">
대구 이곡동에서 만나는 고기의 재발견! 왕갈비 돌판 짜장 + 두툼 탕수육 이색 중식 체험!
</div>

<h2>관련 태그</h2>
<span class="tag">#생생정보</span>
<span class="tag">#결정적한수</span>
<span class="tag">#왕갈비해물돌판짜장</span>
<span class="tag">#대구맛집</span>
<span class="tag">#달서구맛집</span>
<span class="tag">#왕갈비짜장</span>
<span class="tag">#이색중식</span>
<span class="tag">#이곡동맛집</span>
<span class="tag">#성서산업단지역맛집</span>
<span class="tag">#두툼탕수육</span>
<span class="tag">#초당순두부짬뽕</span>
<span class="tag">#KBS생생정보</span>

<p style="margin-top:30px; font-size:13px; color:#999;">※ 본 포스팅은 KBS 2TV 생생정보 방송 내용을 기반으로 작성되었습니다. 방문 전 영업시간과 메뉴를 확인해주세요.</p>

</div>
BODY
        ),

        // ------------------------------------------------------------------ 05
        array(
            'title' => '[생생정보] 서면손두부집 - 춘천 양숙 할머니의 손맛! 야들야들 손두부 정식',
            'style' => $common_style,
            'tags'  => array( '생생정보', '할매밥됩니까', '서면손두부집', '춘천맛집', '손두부', '두부정식', '춘천서면맛집', '강원도맛집', 'KBS생생정보' ),
            'body'  => <<<'BODY'
<div class="saenginfo-post">

<h1>[2TV 생생정보] 서면손두부집 - 춘천 양숙 할머니의 손맛! 야들야들 손두부 정식</h1>

<p class="meta">2026년 2월 20일 방송 | KBS2 2TV 생생정보 | 코너: 할매, 밥 됩니까</p>

<img src="images/05_main.webp" alt="서면손두부집 손두부 정식" style="width:100%; border-radius:10px; margin:20px 0;">

<p>안녕하세요! 오늘은 <strong>2TV 생생정보 '할매, 밥 됩니까'</strong> 코너에서 소개된 <strong>강원 춘천시 서면</strong>의 손두부 맛집 <strong>서면손두부집</strong>을 소개해드리려고 합니다.</p>

<p>춘천 깊은 산골, <strong>양숙 할머니</strong>가 직접 만드는 <strong>야들야들한 손두부</strong>! 매일 새벽 콩을 불리고 맷돌에 갈아 직접 두부를 만드는 정성이 깃든 곳입니다. 매번 바뀌는 정성 가득 반찬과 함께 내어주는 <strong>손두부 정식</strong>은 몸과 마음이 편안해지는 건강한 한 끼입니다.</p>

<div class="highlight-box">
💡 <strong>이 맛집이 특별한 이유:</strong> 매일 새벽 콩을 불리고 맷돌에 갈아 직접 만드는 수제 두부! 양숙 할머니의 오랜 손맛으로 빚어낸 야들야들하고 부드러운 두부는 소화가 잘 되는 건강식이며, 매번 달라지는 정성 가득 반찬이 방문할 때마다 새로운 즐거움을 줍니다.
</div>

<h2>📍 맛집 기본 정보</h2>

<div class="info-card">
<strong>🏪 가게명:</strong> 서면손두부집<br>
<strong>🏠 위치:</strong> 강원도 춘천시 서면 당산길 31-11<br>
<strong>📞 전화:</strong> 033-243-2280<br>
<strong>📺 방송:</strong> 2TV 생생정보 2026.02.20 '할매, 밥 됩니까' 코너<br>
<strong>👩 운영자:</strong> 양숙 할머니<br>
<strong>🅿️ 주차:</strong> 자체 주차 가능<br>
<strong>📌 특이사항:</strong> 매일 새벽 콩 불리고 맷돌에 갈아 직접 두부 제조, 매번 반찬 구성이 바뀜, 소화가 잘 되는 건강식
</div>

<h2>대표 메뉴</h2>

<table class="menu-table">
<tr><th>메뉴</th><th>특징</th></tr>
<tr><td>손두부 정식</td><td>할머니의 손맛으로 직접 만든 야들야들 두부 + 매번 달라지는 반찬 한 상</td></tr>
<tr><td>두부 전골</td><td>뜨끈한 국물에 부드러운 손두부가 듬뿍, 몸 따뜻해지는 보양식</td></tr>
<tr><td>두부구이</td><td>겉은 바삭하고 속은 부드러운 고소한 두부구이</td></tr>
</table>

<img src="images/05_menu.webp" alt="서면손두부집 두부 전골 메뉴" style="width:100%; border-radius:10px; margin:20px 0;">

<h2>실제 방문 후기</h2>

<blockquote style="background:#f1f2f6; padding:15px; border-radius:10px; border-left:4px solid #d63031;">
"두부가 정말 야들야들하고 부드러워요. 반찬도 매번 바뀌는데 하나하나 정성이 느껴집니다. 소화도 잘 되고, 먹고 나면 속이 정말 편해요. 할머니 손맛 최고!"
</blockquote>

<h2>찾아가는 길</h2>

<p><strong>자가용:</strong> 서울춘천고속도로 이용, 춘천IC 진출 후 서면 방면<br>
<strong>대중교통:</strong> 춘천 시외버스터미널에서 서면 방면 시내버스 이용<br>
<strong>주차:</strong> 자체 주차 가능</p>

<iframe src="https://map.kakao.com/?q=%EC%84%9C%EB%A9%B4%EC%86%90%EB%91%90%EB%B6%80%EC%A7%91+%EC%B6%98%EC%B2%9C&map_type=TYPE_MAP&from=roughmap" width="100%" height="350" style="border:none; border-radius:10px; margin:20px 0;"></iframe>
<p style="font-size:13px; color:#999;">📍 강원도 춘천시 서면 당산길 31-11 | ☎ 033-243-2280</p>

<div class="cta">
춘천 여행 + 할매 손두부 정식으로 몸과 마음 모두 힐링하세요!
</div>

<h2>관련 태그</h2>
<span class="tag">#생생정보</span>
<span class="tag">#할매밥됩니까</span>
<span class="tag">#서면손두부집</span>
<span class="tag">#춘천맛집</span>
<span class="tag">#손두부</span>
<span class="tag">#두부정식</span>
<span class="tag">#춘천서면맛집</span>
<span class="tag">#강원도맛집</span>
<span class="tag">#KBS생생정보</span>

<p style="margin-top:30px; font-size:13px; color:#999;">※ 본 포스팅은 KBS 2TV 생생정보 방송 내용을 기반으로 작성되었습니다. 방문 전 영업시간과 메뉴를 확인해주세요.</p>

</div>
BODY
        ),

        // ------------------------------------------------------------------ 06
        array(
            'title' => '[생생정보] 국보1호점 - 13,900원 한우 칼국수+보쌈 무한리필! 부천 힐스테이트 중동 맛집',
            'style' => $common_style,
            'tags'  => array( '생생정보', '가격파괴Why', '국보1호점', '부천맛집', '한우칼국수', '보쌈무한리필', '가성비맛집', '중동맛집', '힐스테이트중동', 'KBS생생정보' ),
            'body'  => <<<'BODY'
<div class="saenginfo-post">

<h1>[2TV 생생정보] 국보1호점 - 13,900원 한우 칼국수+보쌈 무한리필! 부천 힐스테이트 중동 가성비 맛집</h1>

<p class="meta">2026년 2월 11일 방송 | KBS2 2TV 생생정보 | 코너: 가격파괴 Why</p>

<img src="images/06_main.webp" alt="국보1호점 한우 사골 칼국수 보쌈" style="width:100%; border-radius:10px; margin:20px 0;">

<p>요즘 외식비가 부담되시죠? 그런데 <strong>13,900원에 한우 사골 칼국수와 국내산 보쌈 무한리필</strong>을 즐길 수 있는 곳이 있다면 믿으시겠어요?</p>

<p>오늘은 <strong>2TV 생생정보 '가격파괴 Why'</strong> 코너에서 소개된 <strong>경기 부천시 원미구 중동 힐스테이트 중동</strong>의 초특급 가성비 맛집 <strong>국보1호점</strong>을 소개합니다!</p>

<div class="highlight-box">
<div class="price-badge">칼국수+보쌈 무한리필 13,900원</div>
<br><br>
💡 <strong>한우 사골 칼국수 + 보쌈 무한리필!</strong> 진한 사골 육수 베이스의 칼국수와 부드럽고 잡내 없는 국내산 보쌈을 무한으로 즐기세요. 이 가격이 가능한 이유, 방송에서 그 비밀을 공개했습니다!
</div>

<h2>📍 맛집 기본 정보</h2>

<div class="info-card">
<strong>🏪 가게명:</strong> 국보1호점<br>
<strong>🏠 위치:</strong> 경기도 부천시 원미구 길주로 234 203동 1층 1094호 (힐스테이트 중동)<br>
<strong>📞 전화:</strong> 032-651-1566<br>
<strong>💰 가격:</strong> 칼국수+보쌈 무한리필 13,900원(성인) / 9,000원(초등) / 전골칼국수+맛보쌈 세트 10,000원 / 고기·김치만두 5,000원<br>
<strong>🕐 영업시간:</strong> 매일 11:00~21:00 (브레이크타임 15:00~17:00, LO 20:40)<br>
<strong>🅿️ 주차:</strong> 상가 전용 지하 주차장 무료<br>
<strong>🚇 교통:</strong> 신중동역 또는 부천시청역 하차 후 도보<br>
<strong>📺 방송:</strong> 2TV 생생정보 2026.02.11 '가격파괴 Why' 코너<br>
<strong>👥 추천 대상:</strong> 가성비 맛집을 찾는 분, 가족 외식, 직장인 점심
</div>

<h2>대표 메뉴</h2>

<table class="menu-table">
<tr><th>메뉴</th><th>특징</th><th>가격</th></tr>
<tr><td>🥇 칼국수+보쌈 무한리필 (성인)</td><td>한우 사골 칼국수 + 국내산 보쌈 — 무한리필</td><td>13,900원</td></tr>
<tr><td>칼국수+보쌈 무한리필 (초등)</td><td>동일 메뉴, 초등학생 할인가</td><td>9,000원</td></tr>
<tr><td>전골칼국수+맛보쌈 세트</td><td>전골 방식 칼국수 + 맛보쌈 구성</td><td>10,000원</td></tr>
<tr><td>고기만두 / 김치만두</td><td>수제 만두</td><td>5,000원</td></tr>
</table>

<img src="images/06_menu.webp" alt="국보1호점 보쌈 칼국수 메뉴" style="width:100%; border-radius:10px; margin:20px 0;">

<h2>이 맛집의 포인트</h2>

<ul>
<li><strong>가격 파괴 가성비</strong> — 13,900원에 한우 칼국수 + 보쌈 무한리필</li>
<li><strong>진한 사골 육수</strong> — 한우 사골을 오랜 시간 우려낸 깊고 진한 국물</li>
<li><strong>국내산 보쌈 무한리필</strong> — 부드럽고 잡내 없는 보쌈을 원하는 만큼</li>
<li><strong>힐스테이트 중동 내 위치</strong> — 부천 중동 대형 아파트 단지 상가, 전용 지하 주차장 무료</li>
</ul>

<h2>실제 방문 후기</h2>

<blockquote style="background:#f1f2f6; padding:15px; border-radius:10px; border-left:4px solid #d63031;">
"만 원대에 칼국수에 보쌈 무한리필이라니! 사골 육수도 진하고, 보쌈도 부드럽고 잡내가 전혀 없어요. 이 가격에 이 퀄리티는 정말 가격파괴입니다."
</blockquote>

<h2>찾아가는 길</h2>

<p><strong>지하철:</strong> 서울 지하철 7호선 신중동역 또는 부천시청역 하차 후 도보<br>
<strong>버스:</strong> 부천 중동 방면 시내버스 이용<br>
<strong>주차:</strong> 힐스테이트 중동 상가 전용 지하 주차장 무료</p>

<iframe src="https://map.kakao.com/?q=%EA%B5%AD%EB%B3%B41%ED%98%B8%EC%A0%90+%EB%B6%80%EC%B2%9C&map_type=TYPE_MAP&from=roughmap" width="100%" height="350" style="border:none; border-radius:10px; margin:20px 0;"></iframe>
<p style="font-size:13px; color:#999;">📍 경기도 부천시 원미구 길주로 234 203동 1층 1094호 | ☎ 032-651-1566</p>

<div class="cta">
국보1호점 — 13,900원으로 한우 칼국수에 보쌈 무한리필! 부천 힐스테이트 중동 가성비 끝판왕!
</div>

<h2>관련 태그</h2>
<span class="tag">#생생정보</span>
<span class="tag">#가격파괴Why</span>
<span class="tag">#국보1호점</span>
<span class="tag">#부천맛집</span>
<span class="tag">#한우칼국수</span>
<span class="tag">#보쌈무한리필</span>
<span class="tag">#가성비맛집</span>
<span class="tag">#중동맛집</span>
<span class="tag">#힐스테이트중동</span>
<span class="tag">#KBS생생정보</span>

<p style="margin-top:30px; font-size:13px; color:#999;">※ 본 포스팅은 KBS 2TV 생생정보 방송 내용을 기반으로 작성되었습니다. 방문 전 영업시간과 메뉴를 확인해주세요.</p>

</div>
BODY
        ),

        // ------------------------------------------------------------------ 07
        array(
            'title' => '[생생정보] 임자 - 강남 논현동 들깨 생아귀탕! 칼칼+고소한 국물의 비밀',
            'style' => $common_style,
            'tags'  => array( '생생정보', '장사의신', '임자', '강남맛집', '논현동맛집', '생아귀탕', '들깨아귀탕', '맑은아귀탕', '매운아귀탕', '아귀간서비스', '아귀찜', '해물찜', '선정릉역맛집', '강남구청역맛집', 'KBS생생정보' ),
            'body'  => <<<'BODY'
<div class="saenginfo-post">

<h1>🍲 [2TV 생생정보] 임자 - 강남 논현동 들깨 생아귀탕! 칼칼+고소한 국물의 비밀</h1>

<p class="meta">📺 2026년 2월 9일 방송 | KBS2 2TV 생생정보 | 코너: 장사의 신</p>

<img src="images/07_main.jpg" alt="임자 생아귀탕" style="width:100%; border-radius:10px; margin:20px 0;">

<p>안녕하세요! 오늘은 <strong>2TV 생생정보 '장사의 신'</strong> 코너에서 소개된 <strong>서울 강남구 논현동</strong>의 아귀 전문 맛집 <strong>임자</strong>를 소개해드리려고 합니다.</p>

<p>선정릉역과 강남구청역 인근에 위치한 이 맛집의 시그니처 메뉴는 바로 <strong>"생아귀탕"</strong>입니다! 맑은탕·매운탕·들깨탕 세 가지 스타일로 즐길 수 있고, 신선한 생아귀를 사용해 귀한 <strong>아귀 간</strong>을 서비스로 제공하는 것으로도 유명합니다. 🐟</p>

<div class="highlight-box">
💡 <strong>이 맛집이 특별한 이유:</strong> 신선한 생아귀를 사용해 맑은탕·매운탕·들깨탕 삼색으로 즐길 수 있습니다! 국물이 깊고 진하며 아귀살이 부드러워 남녀노소 모두 즐길 수 있습니다. 신선한 생아귀 특유의 귀한 <strong>아귀 간을 서비스</strong>로 제공하는 것이 이 집만의 특별한 매력입니다.
</div>

<h2>📍 맛집 기본 정보</h2>

<div class="info-card">
<strong>🏪 가게명:</strong> 임자<br>
<strong>🏠 위치:</strong> 서울 강남구 논현동 (선정릉역 · 강남구청역 인근)<br>
<strong>📺 방송:</strong> 2TV 생생정보 2026.02.09 '장사의 신' 코너<br>
<strong>🅿️ 주차:</strong> 인근 공영주차장 이용 가능<br>
<strong>📌 특이사항:</strong> 신선한 생아귀 '아귀 간' 서비스 제공, 맑은탕·매운탕·들깨탕 삼색 선택 가능, 점심시간 직장인 방문 많음
</div>

<h2>🍽️ 대표 메뉴</h2>

<table class="menu-table">
<tr><th>메뉴</th><th>특징</th></tr>
<tr><td>🥇 생아귀탕 (맑은탕)</td><td>깔끔하고 시원한 맑은 국물로 즐기는 생아귀탕</td></tr>
<tr><td>생아귀탕 (매운탕)</td><td>칼칼하게 끓여낸 매운 버전의 생아귀탕</td></tr>
<tr><td>생아귀탕 (들깨탕)</td><td>고소한 들깨가 국물에 풍미를 더한 시그니처 생아귀탕</td></tr>
<tr><td>⭐ 아귀 간 (서비스)</td><td>신선한 생아귀만의 특별한 별미 — 무료 서비스 제공</td></tr>
<tr><td>🥈 아귀찜</td><td>매콤달콤한 양념에 쫄깃한 아귀살과 콩나물의 조화</td></tr>
<tr><td>🥉 해물찜</td><td>다양한 신선 해산물이 가득한 푸짐한 해물찜</td></tr>
</table>

<img src="images/07_menu.jpg" alt="임자 생아귀탕 메뉴" style="width:100%; border-radius:10px; margin:20px 0;">

<h2>💬 실제 방문 후기</h2>

<blockquote style="background:#f1f2f6; padding:15px; border-radius:10px; border-left:4px solid #d63031;">
"국물이 정말 칼칼하면서도 들깨 덕분에 고소해요. 아귀살이 부드럽게 녹아서 숟가락이 멈추질 않습니다. 추운 겨울에 딱 좋은 보양식이에요!"
</blockquote>

<h2>🚗 찾아가는 길</h2>

<p>🚇 <strong>지하철:</strong> 선정릉역 또는 강남구청역 하차 후 도보 약 5~10분<br>
🚌 <strong>버스:</strong> 논현동 방면 버스 이용<br>
🅿️ <strong>주차:</strong> 인근 공영주차장 이용</p>

<iframe src="https://map.kakao.com/?q=%EC%9E%84%EC%9E%90+%EA%B0%95%EB%82%A8+%EB%85%BC%ED%98%84%EB%8F%99&map_type=TYPE_MAP&from=roughmap" width="100%" height="350" style="border:none; border-radius:10px; margin:20px 0;"></iframe>
<p style="font-size:13px; color:#999;">📍 서울 강남구 논현동 (선정릉역·강남구청역 인근)</p>

<div class="cta">
🔥 임자 — 강남 논현동 생아귀탕 전문점! 맑은탕·매운탕·들깨탕 삼색 + 아귀 간 서비스까지!
</div>

<h2>🏷️ 관련 태그</h2>
<span class="tag">#생생정보</span>
<span class="tag">#장사의신</span>
<span class="tag">#임자</span>
<span class="tag">#강남맛집</span>
<span class="tag">#논현동맛집</span>
<span class="tag">#생아귀탕</span>
<span class="tag">#들깨아귀탕</span>
<span class="tag">#맑은아귀탕</span>
<span class="tag">#매운아귀탕</span>
<span class="tag">#아귀간서비스</span>
<span class="tag">#아귀찜</span>
<span class="tag">#해물찜</span>
<span class="tag">#선정릉역맛집</span>
<span class="tag">#강남구청역맛집</span>
<span class="tag">#KBS생생정보</span>

<p style="margin-top:30px; font-size:13px; color:#999;">※ 본 포스팅은 KBS 2TV 생생정보 방송 내용을 기반으로 작성되었습니다. 방문 전 영업시간과 메뉴를 확인해주세요.</p>

</div>
BODY
        ),

        // ------------------------------------------------------------------ 08
        array(
            'title' => '[생생정보] 행주추어매운탕 - 김미려 추천! 행주산성 먹거리촌 추어 매운탕 노포',
            'style' => $common_style,
            'tags'  => array( '생생정보', '스타밥집', '행주추어매운탕', '김미려맛집', '고양맛집', '행주동맛집', '추어매운탕', '노포맛집', '통추어', '간추어', '행주산성맛집', '행주산성먹거리촌', 'KBS생생정보' ),
            'body'  => <<<'BODY'
<div class="saenginfo-post">

<h1>🍲 [2TV 생생정보] 행주추어매운탕 - 김미려 추천! 행주산성 먹거리촌 추어 매운탕 노포</h1>

<p class="meta">📺 2026년 2월 5일 방송 | KBS2 2TV 생생정보 | 코너: 스타 밥집 | 추천: 개그우먼 김미려</p>

<img src="images/08_main.jpg" alt="행주추어매운탕" style="width:100%; border-radius:10px; margin:20px 0;">

<p>안녕하세요! 오늘은 <strong>2TV 생생정보 '스타 밥집'</strong> 코너에서 <strong>개그우먼 김미려</strong>님이 추천한 <strong>경기 고양시 덕양구 행주동</strong>의 맛집 <strong>행주추어매운탕</strong>을 소개해드리려고 합니다.</p>

<p>행주산성 먹거리촌에 자리한 이 노포 맛집의 시그니처 메뉴는 바로 <strong>"추어 매운탕"</strong>입니다! 일반 추어탕과는 전혀 다른 매력을 자랑한다고 하는데요. 🐟</p>

<div class="highlight-box">
💡 <strong>이 맛집이 특별한 이유:</strong> 행주의 노포! 일반 추어탕과 달리 맑고 개운하면서도 얼큰한 국물이 특징입니다. 통추어는 2인분 이상 주문해야 하며, 간추어(갈아 만든 추어)는 1인분부터 주문 가능합니다. 수제비와 국수가 국물에 함께 들어가 한 그릇으로 든든한 한 끼를 즐길 수 있습니다. 김미려님이 직접 단골로 다닌다는 검증된 맛집!
</div>

<h2>📍 맛집 기본 정보</h2>

<div class="info-card">
<strong>🏪 가게명:</strong> 행주추어매운탕<br>
<strong>🏠 위치:</strong> 경기 고양시 덕양구 행주동 (행주산성 먹거리촌)<br>
<strong>📺 방송:</strong> 2TV 생생정보 2026.02.05 '스타 밥집' 코너<br>
<strong>⭐ 추천인:</strong> 개그우먼 김미려<br>
<strong>🅿️ 주차:</strong> 매장 주차 가능 (행주산성 인근)<br>
<strong>📌 특이사항:</strong> 행주의 노포, 통추어 2인분 이상 주문 / 간추어 1인분 주문 가능, 행주산성 관광 후 식사 코스로 추천
</div>

<h2>🍽️ 대표 메뉴</h2>

<table class="menu-table">
<tr><th>메뉴</th><th>특징</th></tr>
<tr><td>🥇 추어 매운탕 (통추어)</td><td>맑고 개운하며 얼큰한 국물 + 수제비·국수 함께 제공, 2인분 이상 주문</td></tr>
<tr><td>추어 매운탕 (간추어)</td><td>추어를 갈아 넣은 버전, 1인분부터 주문 가능</td></tr>
<tr><td>🥈 메기 매운탕</td><td>담백하면서도 칼칼한 메기 매운탕</td></tr>
<tr><td>🥉 장어구이</td><td>숯불에 구운 고소하고 쫄깃한 장어</td></tr>
<tr><td>⭐ 매콤 낙지 덮밥</td><td>불맛 가득한 매콤 낙지와 밥의 환상 조합</td></tr>
</table>

<img src="images/08_main.jpg" alt="행주추어매운탕 메뉴" style="width:100%; border-radius:10px; margin:20px 0;">

<h2>💬 실제 방문 후기</h2>

<blockquote style="background:#f1f2f6; padding:15px; border-radius:10px; border-left:4px solid #d63031;">
"추어탕 특유의 텁텁함이 없고, 맑으면서도 얼큰해서 깔끔하게 먹을 수 있어요. 수제비와 국수가 들어 있어 양도 넉넉하고 정말 든든합니다. 추어탕을 싫어하는 사람도 이건 좋아할 맛!"
</blockquote>

<h2>🚗 찾아가는 길</h2>

<p>🚇 <strong>지하철:</strong> 3호선 원당역 또는 화정역 하차 후 버스·택시 환승<br>
🚌 <strong>버스:</strong> 행주산성 방면 버스 이용<br>
🅿️ <strong>주차:</strong> 매장 주차장 이용 가능</p>

<iframe src="https://map.kakao.com/?q=%ED%96%89%EC%A3%BC%EC%B6%94%EC%96%B4%EB%A7%A4%EC%9A%B4%ED%83%95+%EA%B3%A0%EC%96%91&map_type=TYPE_MAP&from=roughmap" width="100%" height="350" style="border:none; border-radius:10px; margin:20px 0;"></iframe>
<p style="font-size:13px; color:#999;">📍 경기 고양시 덕양구 행주동 (행주산성 먹거리촌)</p>

<div class="cta">
🔥 행주추어매운탕 — 행주산성 나들이 + 김미려 추천 노포 추어 매운탕 코스로 완벽한 하루!
</div>

<h2>🏷️ 관련 태그</h2>
<span class="tag">#생생정보</span>
<span class="tag">#스타밥집</span>
<span class="tag">#행주추어매운탕</span>
<span class="tag">#김미려맛집</span>
<span class="tag">#고양맛집</span>
<span class="tag">#행주동맛집</span>
<span class="tag">#추어매운탕</span>
<span class="tag">#노포맛집</span>
<span class="tag">#통추어</span>
<span class="tag">#간추어</span>
<span class="tag">#행주산성맛집</span>
<span class="tag">#행주산성먹거리촌</span>
<span class="tag">#KBS생생정보</span>

<p style="margin-top:30px; font-size:13px; color:#999;">※ 본 포스팅은 KBS 2TV 생생정보 방송 내용을 기반으로 작성되었습니다. 방문 전 영업시간과 메뉴를 확인해주세요.</p>

</div>
BODY
        ),

        // ------------------------------------------------------------------ 09
        array(
            'title' => '[생생정보] 포항할매집 - 3대 70년 전통 영천공설시장 소머리곰탕 백년가게',
            'style' => $common_style,
            'tags'  => array( '생생정보', '할매밥됩니까', '포항할매집', '영천맛집', '영천공설시장', '소머리곰탕', '가마솥곰탕', '3대맛집', '백년가게', '중소벤처기업부백년가게', '뚝배기토렴', '전통시장맛집', '경북맛집', 'KBS생생정보' ),
            'body'  => <<<'BODY'
<div class="saenginfo-post">

<h1>🍲 [2TV 생생정보] 포항할매집 - 3대 70년 전통 영천공설시장 소머리곰탕 백년가게</h1>

<p class="meta">📺 2026년 2월 2일 방송 | KBS2 2TV 생생정보 | 코너: 할매, 밥 됩니까</p>

<img src="images/09_main.jpg" alt="포항할매집 소머리곰탕" style="width:100%; border-radius:10px; margin:20px 0;">

<p>안녕하세요! 오늘은 <strong>2TV 생생정보 '할매, 밥 됩니까'</strong> 코너에서 소개된 <strong>경북 영천시 영천공설시장</strong>의 전설적인 맛집 <strong>포항할매집</strong>을 소개해드리려고 합니다.</p>

<p>3대 70년 전통의 이 백년가게 맛집의 유일무이한 메뉴는 바로 <strong>"소머리곰탕"</strong>입니다! 전국 각지에서 이 곰탕 한 그릇을 먹기 위해 영천시장까지 찾아온다고 합니다. 🐂</p>

<div class="highlight-box">
💡 <strong>이 맛집이 특별한 이유:</strong> 3대 70년 전통의 중소벤처기업부 인증 백년가게! 커다란 가마솥에서 소머리를 푹 고아 뚝배기에 토렴 방식으로 서빙합니다. 잡내가 전혀 없는 깨끗하고 깊은 국물이 핵심 비결! 전국에서 일부러 방문하는 손님이 끊이지 않습니다.
</div>

<h2>📍 맛집 기본 정보</h2>

<div class="info-card">
<strong>🏪 가게명:</strong> 포항할매집<br>
<strong>🏠 위치:</strong> 경상북도 영천시 시장4길 52 (완산동 982-3, 영천공설시장 내)<br>
<strong>💰 가격:</strong> 소머리곰탕 9,000원 / 한우소머리곰탕 10,000원 / 포장 5그릇 20,000원<br>
<strong>🕐 영업시간:</strong> 매일 07:00~20:00 (LO 19:30, 정기휴무: 매월 1일·15일)<br>
<strong>📺 방송:</strong> 2TV 생생정보 2026.02.02 '할매, 밥 됩니까' 코너<br>
<strong>🅿️ 주차:</strong> 영천시장 공영주차장 이용 가능<br>
<strong>📌 특이사항:</strong> 3대 70년 전통, 중소벤처기업부 백년가게 인증, 가마솥 즉석 서빙, 뚝배기 토렴 방식, 전국에서 방문하는 맛집
</div>

<h2>🍽️ 대표 메뉴</h2>

<table class="menu-table">
<tr><th>메뉴</th><th>특징</th><th>가격</th></tr>
<tr><td>🥇 소머리곰탕</td><td>3대 비법 가마솥 곰탕 · 잡내 없는 깊고 진한 국물 · 뚝배기 토렴 서빙</td><td>9,000원</td></tr>
<tr><td>🐄 한우소머리곰탕</td><td>한우 소머리로 끓인 프리미엄 곰탕</td><td>10,000원</td></tr>
<tr><td>📦 포장 (5그릇)</td><td>포장 판매 (5그릇 세트)</td><td>20,000원</td></tr>
</table>

<img src="images/09_menu.jpg" alt="포항할매집 메뉴" style="width:100%; border-radius:10px; margin:20px 0;">

<h2>💬 실제 방문 후기</h2>

<blockquote style="background:#f1f2f6; padding:15px; border-radius:10px; border-left:4px solid #d63031;">
"서울에서 일부러 영천까지 왔는데 정말 후회 없는 맛이에요. 가마솥에서 바로 퍼주니까 국물이 뜨끈뜨끈하고, 잡내가 하나도 없어요. 고기도 푸짐하고 국물이 뽀얗고 깊어서 한 방울도 남기기 아깝습니다. 3대째 이어온 맛은 역시 다르네요!"
</blockquote>

<h2>🚗 찾아가는 길</h2>

<p>🚗 <strong>자가용:</strong> 경부고속도로 영천IC에서 영천시장 방면 약 10분<br>
🚌 <strong>버스:</strong> 영천시외버스터미널 하차 후 영천시장까지 도보 약 10분<br>
🚆 <strong>기차:</strong> KTX/무궁화호 영천역 하차 후 택시 약 5분<br>
🅿️ <strong>주차:</strong> 영천시장 공영주차장 이용</p>

<iframe src="https://map.kakao.com/?q=%ED%8F%AC%ED%95%AD%ED%95%A0%EB%A7%A4%EC%A7%91+%EC%98%81%EC%B2%9C&map_type=TYPE_MAP&from=roughmap" width="100%" height="350" style="border:none; border-radius:10px; margin:20px 0;"></iframe>
<p style="font-size:13px; color:#999;">📍 경상북도 영천시 시장4길 52 (영천공설시장 내)</p>

<div class="cta">
🔥 포항할매집 — 3대 70년 전통 백년가게 가마솥 소머리곰탕! 영천 여행의 필수 코스!
</div>

<h2>🏷️ 관련 태그</h2>
<span class="tag">#생생정보</span>
<span class="tag">#할매밥됩니까</span>
<span class="tag">#포항할매집</span>
<span class="tag">#영천맛집</span>
<span class="tag">#영천공설시장</span>
<span class="tag">#소머리곰탕</span>
<span class="tag">#가마솥곰탕</span>
<span class="tag">#3대맛집</span>
<span class="tag">#백년가게</span>
<span class="tag">#중소벤처기업부백년가게</span>
<span class="tag">#뚝배기토렴</span>
<span class="tag">#전통시장맛집</span>
<span class="tag">#경북맛집</span>
<span class="tag">#KBS생생정보</span>

<p style="margin-top:30px; font-size:13px; color:#999;">※ 본 포스팅은 KBS 2TV 생생정보 방송 내용을 기반으로 작성되었습니다. 방문 전 영업시간과 메뉴를 확인해주세요.</p>

</div>
BODY
        ),

        // ------------------------------------------------------------------ 10
        array(
            'title' => '[생생정보] 시골막국수·홍천잣떡 - 한혜진의 홍천 여행! 막국수+모두부+잣 호떡 맛집 총정리',
            'style' => $common_style,
            'tags'  => array( '생생정보', '스타의고장', '한혜진', '홍천맛집', '시골막국수', '홍천막국수', '모두부', '잣호떡', '홍천여행', '홍천강꽁꽁축제', '알파카월드', '강원도맛집', 'KBS생생정보' ),
            'body'  => <<<'BODY'
<div class="saenginfo-post">

<h1>🍜 [2TV 생생정보] 한혜진의 홍천 여행! 막국수+모두부+잣 호떡 맛집 총정리</h1>

<p class="meta">📺 2026년 1월 13일 방송 | KBS2 2TV 생생정보 | 코너: 믿고 떠나는 스타의 고장 | 출연: 가수 한혜진</p>

<img src="images/10_main.jpg" alt="시골막국수 홍천" style="width:100%; border-radius:10px; margin:20px 0;">

<p>안녕하세요! 오늘은 <strong>2TV 생생정보 '믿고 떠나는 스타의 고장'</strong> 코너에서 <strong>가수 한혜진</strong>님과 함께한 <strong>강원 홍천</strong> 여행을 소개해드리려고 합니다.</p>

<p>겨울의 홍천은 맛집뿐 아니라 <strong>홍천강 꽁꽁축제</strong>, <strong>알파카월드</strong> 등 볼거리와 즐길 거리가 가득한데요. 한혜진님이 직접 찾아간 홍천의 맛집들을 지금부터 하나하나 알려드리겠습니다! 북방면 <strong>시골막국수</strong>의 쫄깃한 막국수와 기절맛 모두부, 그리고 홍천읍의 특산 잣으로 만든 잣떡과 잣 꿀 호떡까지! ❄️</p>

<div class="highlight-box">
💡 <strong>홍천 여행 포인트:</strong> 막국수와 모두부의 환상 조합, 홍천 특산품 잣을 활용한 잣떡과 잣 꿀 호떡까지! 겨울 관광(꽁꽁축제, 알파카월드)과 맛집을 한 번에 즐기는 완벽한 홍천 코스입니다.
</div>

<h2>📍 맛집 1 - 시골막국수 (홍천 북방면)</h2>

<div class="info-card">
<strong>🏪 가게명:</strong> 시골막국수<br>
<strong>🏠 위치:</strong> 강원특별자치도 홍천군 북방면 상화계3길 9<br>
<strong>📞 전화:</strong> 033-434-4313<br>
<strong>📺 방송:</strong> 2TV 생생정보 2026.01.13 '믿고 떠나는 스타의 고장' 코너<br>
<strong>⭐ 출연:</strong> 가수 한혜진<br>
<strong>📌 특이사항:</strong> 모두부를 먹으면 기절한다는 평! 막국수와 함께 필수 주문
</div>

<table class="menu-table">
<tr><th>메뉴</th><th>특징</th></tr>
<tr><td>🥇 막국수</td><td>쫄깃한 메밀면에 시원한 육수, 강원도 정통 막국수</td></tr>
<tr><td>🥈 모두부</td><td>"먹으면 기절한다"는 평! 부드럽고 고소한 수제 모두부</td></tr>
</table>

<img src="images/10_main.jpg" alt="시골막국수 모두부" style="width:100%; border-radius:10px; margin:20px 0;">

<h2>📍 맛집 2 - 잣떡 &amp; 잣 꿀 호떡 (홍천읍)</h2>

<div class="info-card">
<strong>🏪 가게명:</strong> 홍천읍 잣떡·잣 꿀 호떡 가게 (정확한 상호명은 방송 확인 필요)<br>
<strong>🏠 위치:</strong> 강원 홍천군 홍천읍<br>
<strong>📺 방송:</strong> 2TV 생생정보 2026.01.13 '믿고 떠나는 스타의 고장' 코너<br>
<strong>📌 특이사항:</strong> 홍천 특산품 잣을 활용한 특색 있는 간식
</div>

<table class="menu-table">
<tr><th>메뉴</th><th>특징</th></tr>
<tr><td>🥇 잣떡</td><td>홍천 특산 잣이 가득 들어간 고소한 떡</td></tr>
<tr><td>🥈 잣 꿀 호떡</td><td>바삭한 호떡 속에 꿀과 잣이 가득, 겨울 간식으로 최고</td></tr>
</table>

<img src="images/10_main.jpg" alt="홍천 잣떡 잣꿀호떡" style="width:100%; border-radius:10px; margin:20px 0;">

<h2>🎿 홍천 겨울 관광 명소</h2>

<div class="highlight-box">
⛄ <strong>홍천강 꽁꽁축제:</strong> 겨울철 홍천강에서 열리는 대표 축제. 얼음낚시, 눈썰매 등 다양한 체험 가능<br><br>
🦙 <strong>알파카월드:</strong> 귀여운 알파카를 직접 만날 수 있는 동물 테마파크. 가족 나들이에 딱!
</div>

<h2>💬 실제 방문 후기</h2>

<blockquote style="background:#f1f2f6; padding:15px; border-radius:10px; border-left:4px solid #d63031;">
"막국수도 맛있었지만, 모두부가 정말 대박이에요! 부드럽고 고소해서 한 번 먹으면 멈출 수가 없습니다. 잣 꿀 호떡은 겨울에 야외에서 먹으니까 더 맛있더라고요. 홍천강 꽁꽁축제랑 알파카월드까지 한 번에 돌면 완벽한 겨울 여행 코스입니다!"
</blockquote>

<h2>🚗 찾아가는 길</h2>

<p>🚗 <strong>자가용:</strong> 서울양양고속도로 또는 중앙고속도로 이용, 홍천IC 진출<br>
🚌 <strong>버스:</strong> 동서울터미널에서 홍천행 시외버스 이용 (약 1시간 30분 소요)<br>
🅿️ <strong>주차:</strong> 각 맛집 및 관광지 주차장 이용 가능</p>

<iframe src="https://map.kakao.com/?q=%EC%8B%9C%EA%B3%A8%EB%A7%89%EA%B5%AD%EC%88%98+%ED%99%8D%EC%B2%9C+%EB%B6%81%EB%B0%A9%EB%A9%B4&map_type=TYPE_MAP&from=roughmap" width="100%" height="350" style="border:none; border-radius:10px; margin:20px 0;"></iframe>
<p style="font-size:13px; color:#999;">📍 강원특별자치도 홍천군 북방면 상화계3길 9 | ☎ 033-434-4313</p>

<div class="cta">
🔥 한혜진과 함께하는 홍천 겨울 여행! 시골막국수 + 모두부 + 잣 꿀 호떡 + 꽁꽁축제 올인원 코스!
</div>

<h2>🏷️ 관련 태그</h2>
<span class="tag">#생생정보</span>
<span class="tag">#스타의고장</span>
<span class="tag">#한혜진</span>
<span class="tag">#홍천맛집</span>
<span class="tag">#시골막국수</span>
<span class="tag">#홍천막국수</span>
<span class="tag">#모두부</span>
<span class="tag">#잣호떡</span>
<span class="tag">#홍천여행</span>
<span class="tag">#홍천강꽁꽁축제</span>
<span class="tag">#알파카월드</span>
<span class="tag">#강원도맛집</span>
<span class="tag">#KBS생생정보</span>

<p style="margin-top:30px; font-size:13px; color:#999;">※ 본 포스팅은 KBS 2TV 생생정보 방송 내용을 기반으로 작성되었습니다. 방문 전 영업시간과 메뉴를 확인해주세요.</p>

</div>
BODY
        ),

    ); // end return array
}
