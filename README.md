<div align="center">
  <h1>🛡️ GuaranteeBot - Telegram 担保交易管理机器人</h1>
  <p>
    <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
    <img src="https://img.shields.io/badge/Framework-Aiogram-green.svg" alt="Aiogram">
    <img src="https://img.shields.io/badge/Status-Updating-orange.svg" alt="Status">
  </p>
  <p><b>一个功能完善的 Telegram 群组担保管理机器人，提供全套自动化交易保障解决方案。</b></p>
</div>

<hr />

<h3>📁 项目结构</h3>
<pre>
guarantee_bot/
├── config.py          # 本地基础配置文件
├── database.py        # 数据库模块（引导加载远程代码）
├── utils.py           # 工具函数（授权验证、视频处理等）
├── main.py            # 主程序入口
└── sp/                # 视频/GIF 缓存文件夹
</pre>

<h3>✨ 功能特性</h3>
<table width="100%">
  <tr>
    <td width="50%" valign="top">
      <h4>🛡️ 安全与授权</h4>
      <p>💡 <b>联系我们 获取免费授权 至高365天：</b><a href="https://t.me/j3855" target="_blank">@j3855</a></p>
      <ul>
        <li><b>动态授权：</b> 启动需输入验证码，每 10 分钟自动轮询校验状态。</li>
        <li><b>功能锁死：</b> 授权过期后自动限制非管理指令，确保运营安全。</li>
        <li><b>防伪系统：</b> 只有通过机器人验证的群组才显示“官方担保”标识。</li>
      </ul>
    </td>
    <td width="50%" valign="top">
      <h4>💰 押金与验群</h4>
      <ul>
        <li><b>额度管理：</b> 支持加/减总押金，以及单独的扣款/回款逻辑。</li>
        <li><b>超押预警：</b> 实时计算可用额度，在验群消息中高亮提示。</li>
        <li><b>多媒介验群：</b> 支持私聊编号查询或群内快捷回复验群。</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h4>⭐ 信用评级</h4>
      <ul>
        <li><b>星级系统：</b> 管理员通过 <code>+1</code> 或 <code>-1</code> 快速调整信用等级。</li>
        <li><b>视觉展示：</b> 自动根据配置渲染 1-5 颗星级 Emoji 图标。</li>
      </ul>
    </td>
    <td width="50%" valign="top">
      <h4>🕒 自动化群控</h4>
      <ul>
        <li><b>营业管理：</b> “上课”自动解禁，“下课”自动禁言并播报广告。</li>
        <li><b>退押流程：</b> “本群退押”一键开启 24 小时结算闭环并禁言。</li>
      </ul>
    </td>
  </tr>
</table>

<p align="center">🚀 <b>更多功能 正在更新中....</b></p>

<hr />

<h3>🚀 快速开始</h3>
<h4>1. 安装环境依赖</h4>
<pre>pip install aiogram aiohttp pycryptodome</pre>

<h4>2. 配置参数</h4>
<p>在 <code>config.py</code> 中填入你的 <code>API_ID</code>, <code>API_HASH</code> 以及机器人 <code>TOKEN</code>。</p>

<hr />

<h3>☕ 捐赠支持 (Donation)</h3>
<p>如果您觉得这个项目对您有所帮助，欢迎打赏支持项目维护：</p>
<ul>
  <li><b>TRC20 (USDT):</b> <code>TDCh5PsfFrj9NrhR7YaS8BVDsmDp888888</code></li>
</ul>

<hr />

<h3>📞 联系我们</h3>
<p>如有疑问或需定制功能，请点击下方链接联系技术支持：</p>
<ul>
  <li><b>官方客服：</b> <a href="https://t.me/j3855" target="_blank">@j3855</a></li>
  <li><b>意见反馈：</b> 联系我们 <a href="https://t.me/j3855" target="_blank">@j3855</a> 传递更新意见和反馈 bug</li>
</ul>

<hr />

<div align="center">
  <p>© 2026 小涵团队 ©版权所有</p>
</div>
