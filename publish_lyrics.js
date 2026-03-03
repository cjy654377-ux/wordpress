const fs = require('fs');
const https = require('https');

const SITE = 'https://rhythmicaleskimo.com';
const REST = SITE + '/wp-json/wp/v2';

function request(method, url, data, cookies) {
  return new Promise((resolve, reject) => {
    const u = new URL(url);
    const opts = {
      hostname: u.hostname,
      path: u.pathname + u.search,
      method: method,
      headers: {}
    };
    if (cookies) opts.headers['Cookie'] = cookies;
    if (data && typeof data === 'string') {
      opts.headers['Content-Type'] = 'application/x-www-form-urlencoded';
      opts.headers['Content-Length'] = Buffer.byteLength(data);
    } else if (data && Buffer.isBuffer(data)) {
      // handled by caller
    } else if (data && typeof data === 'object') {
      const json = JSON.stringify(data);
      opts.headers['Content-Type'] = 'application/json';
      opts.headers['Content-Length'] = Buffer.byteLength(json);
      data = json;
    }
    const req = https.request(opts, (res) => {
      let body = '';
      res.on('data', c => body += c);
      res.on('end', () => resolve({ status: res.statusCode, headers: res.headers, body }));
    });
    req.on('error', reject);
    if (data) req.write(data);
    req.end();
  });
}

async function apiReq(method, path, data, cookies, nonce) {
  return new Promise((resolve, reject) => {
    const u = new URL(REST + path);
    const opts = {
      hostname: u.hostname,
      path: u.pathname + u.search,
      method,
      headers: {
        'Cookie': cookies,
        'X-WP-Nonce': nonce
      }
    };
    let body = null;
    if (data && data.isImage) {
      opts.headers['Content-Type'] = 'image/png';
      opts.headers['Content-Disposition'] = 'attachment; filename=' + data.filename;
      opts.headers['Content-Length'] = data.buffer.length;
      body = data.buffer;
    } else if (data) {
      body = JSON.stringify(data);
      opts.headers['Content-Type'] = 'application/json';
      opts.headers['Content-Length'] = Buffer.byteLength(body);
    }
    const req = https.request(opts, (res) => {
      let b = '';
      res.on('data', c => b += c);
      res.on('end', () => {
        try { resolve({ status: res.statusCode, data: JSON.parse(b) }); }
        catch(e) { resolve({ status: res.statusCode, data: b }); }
      });
    });
    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}

async function main() {
  // Login
  let r = await request('POST', SITE + '/wp-login.php',
    'log=cjy654377%40gmail.com&pwd=Tony2026%21%21&wp-submit=Log+In&redirect_to=%2Fwp-admin%2F&testcookie=1',
    'wordpress_test_cookie=WP+Cookie+check');

  const setCookies = r.headers['set-cookie'] || [];
  const cookies = setCookies.map(c => c.split(';')[0]).join('; ') + '; wordpress_test_cookie=WP+Cookie+check';
  console.log('Login:', r.status === 302 ? 'OK' : 'FAIL ' + r.status);

  // Get nonce
  r = await request('GET', SITE + '/wp-admin/post-new.php', null, cookies);
  const nonceMatch = r.body.match(/"nonce":"([a-f0-9]+)"/);
  if (!nonceMatch) { console.log('Nonce not found'); return; }
  const nonce = nonceMatch[1];
  console.log('Nonce:', nonce);

  const articles = [
    {
      html: 'article_bts_black_swan_lyrics.html',
      img: 'featured_black_swan.png',
      title: 'BTS Black Swan Lyrics Meaning: When Music Becomes Your First Death',
      tags: ['BTS','Black Swan','K-Pop Lyrics','Map of the Soul','Carl Jung','Korean Translation'],
      excerpt: 'BTS Black Swan explores the fear every artist dreads - losing passion for their craft. Korean lyrics with romanization, English translation, and Jungian shadow symbolism.'
    },
    {
      html: 'article_bts_fake_love_lyrics.html',
      img: 'featured_fake_love.png',
      title: 'BTS Fake Love Lyrics Meaning: The Pain of Erasing Yourself to Be Loved',
      tags: ['BTS','Fake Love','K-Pop Lyrics','Love Yourself','Korean Translation','Self Love'],
      excerpt: 'BTS Fake Love is not a breakup song - it is about self-erasure. Full Korean lyrics breakdown with romanization, English meaning, and the Love Yourself trilogy.'
    },
    {
      html: 'article_bts_bst_lyrics.html',
      img: 'featured_bst.png',
      title: 'BTS Blood Sweat & Tears Lyrics Meaning: Demian, Abraxas & the Art of Temptation',
      tags: ['BTS','Blood Sweat Tears','K-Pop Lyrics','Demian','Hermann Hesse','Korean Translation','WINGS'],
      excerpt: 'BTS Blood Sweat & Tears brought Hermann Hesse to K-pop fans. Korean lyrics analysis with the Demian connection, Abraxas symbolism, and MV breakdown.'
    }
  ];

  for (const art of articles) {
    // Upload image
    const imgBuf = fs.readFileSync(art.img);
    const imgRes = await apiReq('POST', '/media', { isImage: true, buffer: imgBuf, filename: art.img }, cookies, nonce);
    const imgId = imgRes.status === 201 ? imgRes.data.id : null;
    console.log('Image:', art.img, imgId ? 'ID=' + imgId : 'FAIL ' + imgRes.status);

    // Create/get tags
    const tagIds = [];
    for (const t of art.tags) {
      let sr = await apiReq('GET', '/tags?search=' + encodeURIComponent(t), null, cookies, nonce);
      if (sr.data && Array.isArray(sr.data) && sr.data.length > 0) {
        tagIds.push(sr.data[0].id);
      } else {
        let cr = await apiReq('POST', '/tags', { name: t }, cookies, nonce);
        if (cr.status === 201) tagIds.push(cr.data.id);
      }
    }

    // Publish
    const content = fs.readFileSync(art.html, 'utf8');
    const postData = {
      title: art.title,
      content: content,
      status: 'publish',
      categories: [96],
      tags: tagIds,
      excerpt: art.excerpt
    };
    if (imgId) postData.featured_media = imgId;

    const pr = await apiReq('POST', '/posts', postData, cookies, nonce);
    if (pr.status === 201) {
      console.log('Published:', art.title.substring(0, 60));
      console.log('  URL:', pr.data.link);
    } else {
      console.log('FAIL:', pr.status, pr.data.message || '');
    }
    console.log('---');
  }
}

main().catch(console.error);
