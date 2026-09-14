# 番茄工作钟 · PWA

把你设计好的番茄钟原型，升级成一个**能装到手机桌面、离线可用、独立窗口运行**的 App。

不需要 Xcode、不需要 Android Studio、不需要上架审核。一个文件夹上传到任意静态托管，手机上「添加到主屏幕」就是一个 App。

---

## 一、这个包里有什么

```
pomodoro-focus-pwa/
├── index.html              应用本体（V2 全部功能 + PWA 能力）
├── manifest.json           App 身份：名字、图标、启动方式、快捷方式
├── sw.js                   Service Worker：离线缓存
├── icons/
│   ├── icon-192.png        图标 192（Android / manifest）
│   ├── icon-512.png        图标 512（Android / 启动画面）
│   ├── apple-touch-icon.png 图标 180（iPhone 主屏）
│   ├── favicon-64.png      浏览器标签页图标
│   └── _gen.py             图标生成脚本（想换图标改这个再跑一遍）
└── README.md               本文件
```

---

## 二、怎么跑起来

### 本地预览（必须用 HTTP，不能双击打开）

Service Worker 和「添加到主屏幕」要求 HTTP/HTTPS 协议，`file://` 直接打开会失效。

```bash
cd pomodoro-focus-pwa
python3 -m http.server 8080
```

然后浏览器打开 `http://localhost:8080`。

### 手机预览（同一 WiFi）

```bash
python3 -m http.server 8080 --bind 0.0.0.0
# 查一下本机 IP：ipconfig getifaddr en0
```

手机浏览器访问 `http://<你的电脑IP>:8080`。
注意：**iPhone Safari 在 HTTP 下不允许添加到主屏幕**，手机实测请用下面的公网部署方案。

---

## 三、部署到公网（三选一）

| 方案 | 耗时 | 适合 | 命令 |
|---|---|---|---|
| **Vercel** | 1 分钟 | 最快，自带 HTTPS | `npx vercel --prod` 然后选目录 |
| **Netlify Drop** | 30 秒 | 不想装东西，拖拽上传 | 打开 app.netlify.com/drop 拖整个文件夹 |
| **GitHub Pages** | 5 分钟 | 想长期维护 / 有仓库 | 推到仓库 → Settings → Pages → 选 main 分支根目录 |

三个都自带 HTTPS，装到手机后离线也能用（首次打开需联网缓存一次）。

---

## 四、装到手机桌面

### iPhone / Safari
1. Safari 打开部署后的网址
2. 点底部**分享按钮** ⬆️
3. 下滑选 **「添加到主屏幕」**
4. 命名 → 添加

装好后：独立图标、全屏无浏览器地址栏、有自己的启动画面。

### Android / Chrome
1. Chrome 打开网址
2. 右上角 **⋮** → **「安装应用」** / 「添加到主屏幕」
3. 或页面底部会自动弹出安装提示条，点「安装」

### 桌面 Chrome / Edge
地址栏右侧会出现安装图标 ⊕，点一下就是独立窗口应用。

---

## 五、功能清单

### 原有（V1）
- 工作 25 / 短休 5 / 长休 15 分钟，时长可调
- 每 2 个番茄进入一次长休（循环）
- 开始 / 暂停 / 跳过 / 重置
- 完成番茄数统计
- 声音提示（Web Audio 合成，无需音频文件）+ 系统通知
- 进度环 + 阶段标识 + 剩余时间

### V2 增量
- **多任务标签**：给每个番茄命名，统计页看各标签分布
- **深色模式自动切换**：跟随系统 / 强制亮 / 强制暗，支持日落规则（18:30 转暗），450ms 过渡
- **灵动岛 / 锁屏状态**：
  - 页面内的灵动岛浮窗（可拖动，显示倒计时 + 暂停/跳过）
  - 浏览器画中画浮窗（Chrome / Edge 支持）
  - Media Session 锁屏媒体控制（支持的浏览器上锁屏可操作）
  - 不支持时自动降级为系统通知，并在设置页说明原因

### 本次新增的 PWA 能力
- **可安装**：添加到主屏幕，独立图标 + 全屏运行
- **离线可用**：Service Worker 缓存核心资产，断网照样计时
- **快捷方式**：长按 App 图标 → 「开始一个番茄」/「查看统计」
- **安装引导条**：浏览器中首次访问时自动提示安装
- **安全区适配**：适配 iPhone 刘海 / 灵动岛 / 底部 Home Indicator

---

## 六、已知限制

| 限制 | 说明 |
|---|---|
| 画中画浮窗 | 仅 Chrome / Edge 桌面版支持；Safari 和移动端不支持，已自动降级为系统通知 |
| 后台计时精度 | 移动端浏览器切后台可能限制定时器。当前实现基于时间戳计算剩余时间，切回来会校正，不会累积误差 |
| iPhone 添加到主屏幕 | 必须 HTTPS，且只能通过 Safari 操作 |
| iOS 通知 | iOS 16.4+ 的 Safari 才支持 Web Push；添加到主屏幕后支持更好 |
| 数据存储 | 存在浏览器 localStorage，卸载重装或清缓存会丢失 |

---

## 七、想改点东西

| 想改什么 | 改哪 |
|---|---|
| 默认时长 | `index.html` 里 `config` 对象的 `work` / `short` / `long` |
| 配色 | `index.html` 顶部的 `:root` / `[data-theme="dark"]` CSS 变量 |
| 图标 | 改 `icons/_gen.py` 里的绘制参数，然后 `python3 icons/_gen.py` |
| App 名字 | `manifest.json` 的 `name` / `short_name`；`index.html` 的 `<title>` 和 `apple-mobile-web-app-title` |
| 离线缓存策略 | `sw.js` 里修改 `VERSION`（改了就会重新拉缓存） |

---

## 八、更新版本时的注意事项

改了 `index.html` 或图标后，记得**同时改 `sw.js` 里的 `VERSION`** 字符串（比如 `v2.1.0` → `v2.1.1`）。否则用户浏览器会继续用旧缓存，看不到更新。

改完重新部署，用户下次打开就是新版。
