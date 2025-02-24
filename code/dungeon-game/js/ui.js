// ui.js
export function updateUI(player) {
    // 更新状态栏
    document.getElementById('hp-value').textContent = `${player.currentHp}/${player.maxHp}`;
    document.getElementById('gold-value').textContent = player.gold;
    document.getElementById('floor-value').textContent = player.floor;

    // 更新血条进度
    const hpPercent = (player.currentHp / player.maxHp) * 100;
    document.getElementById('hp-bar').style.width = `${hpPercent}%`;

    // 更新装备栏
    const inventoryList = document.getElementById('inventory-list') || { innerHTML: '' };

    inventoryList.innerHTML = player.inventory
        .map(item => `<li>${item}</li>`)
        .join('');
}

export function logEvent(player, message) {  // 增加player参数
    const logElement = document.getElementById('event-log');
    const entry = document.createElement('div');
    entry.className = 'log-entry';
    entry.textContent = `[第${player.floor}层] ${message}`;  // 直接使用player参数
    logElement.appendChild(entry);
    logElement.scrollTop = logElement.scrollHeight;
}

// 初始化UI组件
export function initUI() {
    // 创建基础DOM结构（如果未在HTML中预定义）
    if (!document.getElementById('status-bar')) {
        const app = document.getElementById('app');

        // 状态栏
        const statusBar = document.createElement('div');
        statusBar.id = 'status-bar';
        statusBar.innerHTML = `
            <div class="status-item">
                <span>生命值</span>
                <div class="hp-container">
                    <div id="hp-bar" class="hp-bar"></div>
                    <span id="hp-value" class="hp-text">0/100</span>
                </div>
            </div>
            <div class="status-item">
                <span>金币</span>
                <div id="gold-value">0</div>
            </div>
            <div class="status-item">
                <span>当前层数</span>
                <div id="floor-value">1</div>
            </div>
        `;

        // 操作面板
        const controlPanel = document.createElement('div');
        controlPanel.id = 'control-panel';
        controlPanel.innerHTML = `
            <button id="explore-btn">探索</button>
            <button id="shop-btn">商店</button>
        `;

        // 事件日志
        const eventLog = document.createElement('div');
        eventLog.id = 'event-log';

        app.append(statusBar, controlPanel, eventLog);

        // 新增装备栏
        const inventory = document.createElement('div');
        inventory.id = 'inventory-container';
        inventory.innerHTML = `
            <h3>装备栏</h3>
            <ul id="inventory-list"></ul>
        `;
        app.append(inventory);
    }
}
