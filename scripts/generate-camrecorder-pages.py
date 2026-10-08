"""Generate only CamRecorder's support and privacy pages. Run from any directory."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
SITE = 'https://justcompress.online/apps/camrecorder'
EMAIL = 'abel0911@icloud.com'
DATE = 'October 8, 2026'

support = '''<h1>Simple recording.<br>Clear answers.</h1>
<p class="lead">Record video. Take photos. Save on your Mac.</p>
<section><h2>How do I record?</h2><p>Choose your camera and microphone, then select Record video. Select Stop &amp; save to finish. Videos save automatically as MOV files to your chosen folder, at up to 1080p depending on your camera.</p>
<h2>Can I take photos?</h2><p>Use the camera button or Command-P. Photos save as JPG files in the same folder. You can also take a photo while recording.</p>
<h2>Where are my files?</h2><p>Click the saved confirmation to reveal your latest capture in Finder. The menu bar also offers Open recordings folder.</p>
<h2>Camera or microphone unavailable?</h2><p>Open System Settings → Privacy &amp; Security → Camera or Microphone. Allow CamRecorder, then reopen the app. Select your camera and microphone in CamRecorder.</p>
<h2>What is free?</h2><p>Record video and take photos without local background blur or screen light. Both effects can be previewed for free. Purchase CamRecorder Plus to capture with either effect enabled. Plus is a one-time purchase, with no subscription. Apple system video effects remain free.</p>
<h2>How do I restore Plus?</h2><p>Use the Apple Account that purchased Plus and select Restore purchase in the Plus window. If the product cannot load, check your connection and select Retry.</p>
<h2>How does screen light work?</h2><p>CamRecorder uses a display as a light source. It prefers an external display when connected; otherwise it uses the built-in display. Adjust the color, brightness, and light-window size in the app. Color temperatures are approximate presets.</p>
<h2>Why does blur vary?</h2><p>Background blur uses local person segmentation. Lighting, quick movement, hair, and objects crossing the person can affect edges. Adjust the strength before recording. Blur settings are frozen during a recording.</p>
<h2>Can I record from the menu bar?</h2><p>After setup, start recording or select Stop &amp; save from the menu bar camera icon. Closing an idle main window keeps the app available in the menu bar. Select Quit CamRecorder to exit. Pause is not supported.</p>
<h2>Requirements</h2><p>macOS 14 or later. Capture resolution depends on your camera.</p>
<h2>Need more help?</h2><p>Email <a href="mailto:abel0911@icloud.com">abel0911@icloud.com</a> with your macOS version, app version, and a description of the issue. You do not need to send a recording.</p></section>
<section lang="zh-Hans"><h2>中文帮助</h2><p>选择摄像头和麦克风，点击 Record video 开始录制，再点击 Stop &amp; save 停止并自动保存。点击相机按钮或按 Command-P 拍照，录制时也可以拍。</p><p>文件保存在你选择的文件夹。点击保存提示可在 Finder 中查看最新文件；菜单栏也可以打开录制文件夹。</p><p>无法使用相机或麦克风时，请在系统设置 → 隐私与安全性中允许 CamRecorder 使用，然后重新打开应用。</p><p>普通录视频和拍照片免费。本地背景虚化和屏幕补光可免费预览，带这些效果拍摄需要 Plus。Plus 一次购买，无需订阅；已购买用户可在 Plus 窗口点击 Restore purchase 恢复购买。</p><p>补光优先使用连接的外接屏，没有外接屏时使用内置屏。颜色、亮度和补光窗口大小可调。虚化效果受光线、动作及边缘遮挡影响。</p><p>需要 macOS 14 或更新版本。如需帮助，请联系 <a href="mailto:abel0911@icloud.com">abel0911@icloud.com</a>，说明系统版本、应用版本及问题，无需发送录制内容。</p></section>'''

privacy = '''<h1>Your camera.<br>Your files. Your Mac.</h1>
<p class="lead">CamRecorder Privacy Policy</p>
<p>Effective date: October 8, 2026 · Developer: Jiali Liang / Kila Labs</p>
<section><h2>Local camera and audio processing</h2><p>CamRecorder processes camera video, microphone audio, and photos locally on your Mac. The app does not upload your captures to the developer or to a cloud AI service.</p>
<h2>Background blur</h2><p>CamRecorder uses Apple's Vision framework to separate a person from the background and Core Image to blur the background locally. Segmentation masks are used in memory for rendering and are not saved as separate files or transmitted by the app. CamRecorder does not perform facial identification, create facial identity templates, or identify who is in a recording. Photos and videos you capture may contain faces and are saved only to your selected folder.</p>
<h2>Permissions</h2><p>Camera access enables preview, recording, and photos. Microphone access enables audio recording. File access lets CamRecorder save captures to your chosen folder and remember that folder. You can manage camera and microphone permissions in macOS System Settings.</p>
<h2>Local storage</h2><p>Your videos and photos remain in your chosen folder until you move or delete them. App preferences, camera and microphone selection, and folder-access bookmarks are stored locally. StoreKit maintains purchase transactions, and the app checks Plus access. If your selected folder is synced by iCloud Drive or another service, that service's privacy policy applies to its syncing.</p>
<h2>Purchases</h2><p>Apple processes CamRecorder Plus purchases and restores through the App Store. CamRecorder uses StoreKit to verify access for your Apple Account. The app does not provide your payment-card information to the developer. See <a href="https://www.apple.com/legal/privacy/">Apple's privacy policy</a>.</p>
<h2>Analytics and advertising</h2><p>CamRecorder has no advertising or third-party analytics SDKs and does not send usage analytics to the developer.</p>
<h2>Support email</h2><p>If you email us, we receive your email address and the information you choose to send. We use this information to respond to your request. Avoid sending recordings or other personal content unless necessary for the issue. You can request deletion of support correspondence, subject to applicable retention obligations.</p>
<h2>This website</h2><p>These support and privacy pages are hosted on GitHub Pages. They include no analytics scripts, advertising, or forms. GitHub may log visitors' IP addresses for security. This website hosting is separate from camera processing in the Mac app. See the <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub privacy statement</a>.</p>
<h2>Changes and contact</h2><p>We update this page when CamRecorder's privacy practices change. Privacy questions and deletion requests: <a href="mailto:abel0911@icloud.com">abel0911@icloud.com</a>.</p></section>
<section lang="zh-Hans"><h2>中文隐私说明</h2><p>生效日期：2026 年 10 月 8 日。开发者：Jiali Liang / Kila Labs。</p><p>摄像头视频、麦克风音频、照片及背景虚化均在你的 Mac 本地处理。应用不会将拍摄内容上传给开发者或云端 AI 服务。</p><p>背景虚化使用 Apple Vision 人像分割和 Core Image。分割遮罩仅在内存中用于渲染，不另存为文件，也不由应用传输。应用不进行人脸身份识别，不创建人脸身份模板。你保存的照片和视频可能包含人脸，文件保存在你选择的文件夹。</p><p>相机权限用于预览和拍摄，麦克风权限用于录音，文件权限用于保存文件和记住所选文件夹。偏好设置、设备选择和文件夹访问书签保存在本地。你可以在系统设置管理相机及麦克风权限。同步文件夹的行为适用对应同步服务的隐私政策。</p><p>Plus 购买和恢复由 Apple 处理，应用通过 StoreKit 验证权限。开发者不会通过应用收到你的银行卡信息。应用没有广告或第三方统计 SDK，不向开发者发送使用统计。</p><p>支持邮件会向我们提供你的邮箱及你主动发送的信息，用于回复问题。你可以联系我们请求删除支持邮件，但适用的保留义务可能要求保留部分记录。</p><p>本支持和隐私网站由 GitHub Pages 托管，没有统计脚本、广告或表单。GitHub 可能出于安全目的记录访问者 IP；此网站托管与 Mac 应用的本地相机处理相互独立。</p><p>隐私问题及删除请求：<a href="mailto:abel0911@icloud.com">abel0911@icloud.com</a>。</p></section>'''

style = '''body{margin:0;background:#faf7f0;color:#222624;font:17px/1.65 system-ui,-apple-system,sans-serif}main{max-width:860px;margin:auto;padding:32px 24px 56px}nav{display:flex;gap:24px;align-items:center;flex-wrap:wrap;margin-bottom:60px}nav a{color:#222624;text-decoration:none}.brand{font-weight:800;font-size:22px;margin-right:auto}.mark{display:inline-block;width:18px;height:18px;border:6px solid #ff6a50;border-radius:50%;vertical-align:middle;margin-right:10px}h1{font-size:clamp(42px,7vw,76px);line-height:1.06;letter-spacing:-.05em;margin:0 0 24px}h2{font-size:23px;line-height:1.3;margin-top:30px}.lead{font-size:22px;color:#5b625d}section{background:#fff;border:1px solid #e9e4db;border-radius:20px;padding:12px 30px 26px;margin-top:26px}a{color:#ab321c;text-underline-offset:3px}footer{padding-top:30px;color:#626b63;font-size:14px}@media(max-width:540px){nav{gap:16px;margin-bottom:38px}section{padding:8px 20px 20px}.brand{width:100%}}'''

for slug, title, body in [('support', 'CamRecorder Support', support), ('privacy', 'CamRecorder Privacy Policy', privacy)]:
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)}</title><meta name="description" content="{escape(title)} — camera recording and photos on your Mac."><link rel="canonical" href="{SITE}/{slug}/"><style>{style}</style></head><body><main><nav><a class="brand" href="{SITE}/support/"><span class="mark" aria-hidden="true"></span>CamRecorder</a><a href="{SITE}/support/">Support</a><a href="{SITE}/privacy/">Privacy</a></nav>{body}<footer>CamRecorder · macOS 14+ · Jiali Liang / Kila Labs<br><a href="{SITE}/support/">Support</a> · <a href="{SITE}/privacy/">Privacy Policy</a></footer></main></body></html>'''
    target = ROOT / 'apps/camrecorder' / slug / 'index.html'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(page, encoding='utf-8')
    print(target.relative_to(ROOT))
