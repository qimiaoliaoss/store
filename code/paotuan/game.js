// game.js

const realmThresholds = {
    "凡人": 0,
    "开化": 500,
    "筋骨": 1000,
    "锻体": 5000,
    "炼气": 10000,
    "入窍": 20000,
    "通神": 50000,
    "金丹": 100000,
    "元婴": 200000,
    "化神": 500000,
};

// 每个境界对应的灵力增加速度
const spiritIncreaseSpeeds = {
    "凡人": 0, // 凡人境界不增加灵力
    "开化": 1, // 开化境每秒增加1点灵力
    "筋骨": 5, // 筋骨境每秒增加5点灵力
    "锻体": 10, // 锻体境每秒新增10点灵力
    "炼气": 20, // 炼气境每秒新增20点灵力
    "入窍": 30, // 入窍境每秒新增30点灵力
    "通神": 40, // 通神境每秒新增40点灵力
    "金丹": 50, // 金丹境每秒新增50点灵力
    "元婴": 100, // 元婴境每秒新增100点灵力
    "化神": 150, // 化神境每秒新增150点灵力
};

// 突破到某个境界时的效果
function onRealmUpgrade(realm) {
    const spiritIncreaseSpeed = spiritIncreaseSpeeds[realm] || 20; // 默认每秒增加20点灵力
    startAutoIncreaseSpirit(spiritIncreaseSpeed);

    // 判断玩家当前灵力是否超过了突破到下一个境界所需的灵力阈值
    const nextRealm = getNextRealm(realm);
    if (nextRealm) {
        const threshold = realmThresholds[nextRealm];
        if (playerData.spirit >= threshold) {
            // 如果灵力超过了阈值，则继续保留超过的灵力值
            playerData.spirit = playerData.spirit - threshold;
            playerData.realm = nextRealm;
            onRealmUpgrade(playerData.realm); // 触发自动增加灵力的效果
        }
    }
}

// 开始自动增加灵力
let spiritIncreaseInterval; // 保存自动增加灵力的Interval ID

function startAutoIncreaseSpirit(speed) {
    stopAutoIncreaseSpirit(); // 确保只有一个自动增加灵力的Interval在运行
    spiritIncreaseInterval = setInterval(() => {
        playerData.spirit += speed;
        updateUI();
        savePlayerData();
    }, 1000); // 每秒钟增加一次灵力
}

// 停止自动增加灵力
function stopAutoIncreaseSpirit() {
    clearInterval(spiritIncreaseInterval);
}

function setCookie(name, value) {
    document.cookie = `${name}=${value}; expires=Fri, 31 Dec 9999 23:59:59 GMT; path=/`;
}

function getCookie(name) {
    const cookieValue = document.cookie.match(`(^|;)\\s*${name}\\s*=\\s*([^;]+)`);
    return cookieValue ? cookieValue.pop() : '';
}

let playerData = {
    spirit: 0,
    currency: 0,
    equipment1: "无",
    equipment2: "无",
    durability1: 0,
    durability2: 0,
    realm: "凡人", // 设置默认境界为"凡人"
};

function savePlayerData() {
    setCookie("playerData", JSON.stringify(playerData));
}

function loadPlayerData() {
    const data = getCookie("playerData");
    if (data) {
        playerData = JSON.parse(data);
    }
    onRealmUpgrade(playerData.realm); // 在加载玩家数据后重新设置自动增加灵力的效果
    updateUI(); // 更新 UI 显示
}

function resetGame() {
    playerData = {
        spirit: 0,
        currency: 0,
        equipment1: "无",
        equipment2: "无",
        durability1: 0,
        durability2: 0,
    };
    updateUI();
    savePlayerData();
}

function updateUI() {
    document.getElementById("spirit").textContent = playerData.spirit;
    document.getElementById("currency").textContent = playerData.currency;
    document.getElementById("equipment1").textContent = playerData.equipment1;
    document.getElementById("equipment2").textContent = playerData.equipment2;
    document.getElementById("durability1").textContent = playerData.durability1;
    document.getElementById("durability2").textContent = playerData.durability2;
    document.getElementById("shopCurrency").textContent = playerData.currency;

    // 特殊处理灵力为0的情况
    if (playerData.spirit === 0) {
        document.getElementById("realm").textContent = "凡人"; // 灵力为0时显示为"凡人"
        document.getElementById("nextRealmThreshold").textContent = realmThresholds["锻体"]; // 灵力为0时下一境界所需灵力为"锻体"的阈值
    } else {
        document.getElementById("realm").textContent = playerData.realm; // 显示当前境界
        document.getElementById("nextRealmThreshold").textContent = realmThresholds[getNextRealm(playerData.realm)]; // 显示下一境界所需的灵力值
    }
}


function meditate() {
    playerData.spirit += 1; // 模拟冥想获得灵力
    updateUI();
    savePlayerData();
}

function outdoorTraining() {
    if (playerData.spirit > 0) {
        const consumedSpirit = Math.floor(Math.random() * playerData.spirit) + 1; // 消耗的灵力数量在1~当前灵力值之间
        const chance = Math.random(); // 外出历练的成功概率

        if (chance < 0.5) {
            if (consumedSpirit >= playerData.spirit) {
                // 检查玩家是否携带了“药”道具，如果有则询问是否使用
                if (playerData.equipment1 === "药") {
                    if (confirm("外出历练失败，是否消耗一份药来抵消灵力清零？")) {
                        playerData.equipment1 = "无"; // 使用药物后，将药物从装备栏中移除
                    } else {
                        playerData.spirit = 0;
                    }
                } else {
                    playerData.spirit = 0;
                }
                updateUI();
                savePlayerData();
                if (playerData.spirit === 0) {
                    alert("外出历练失败，灵力消耗殆尽！");
                }
            } else {
                playerData.spirit -= consumedSpirit;

                // 检查玩家是否携带了“剑”道具，如果有则额外增加获得的灵石数量
                    let gainedCurrency = Math.floor(Math.random() * 6) + 5; // 获得的灵石数量在5~10之间
                    if (playerData.equipment1 === "剑") {
                        gainedCurrency += 5; // 剑增加额外的5个灵石
                        // 剑的耐久度降低
                        playerData.durability1 -= 1;
                        // 检查剑的耐久度是否耗尽
                        if (playerData.durability1 <= 0) {
                            playerData.equipment1 = "无";
                            playerData.durability1 = 0;
                            alert("剑已损坏，需要重新购买。");
                        }
                    }
                    if (playerData.equipment2 === "剑") {
                        gainedCurrency += 5; // 剑增加额外的5个灵石
                        // 剑的耐久度降低
                        playerData.durability2 -= 1;
                        // 检查剑的耐久度是否耗尽
                        if (playerData.durability2 <= 0) {
                            playerData.equipment2 = "无";
                            playerData.durability2 = 0;
                            alert("剑已损坏，需要重新购买。");
                        }
                    }

                    playerData.currency += gainedCurrency;

                updateUI();
                savePlayerData();
                alert(`外出历练成功！消耗了${consumedSpirit}灵力，获得了${gainedCurrency}灵石！`);
            }
        } else {
            alert("外出历练没有获得任何灵石。");
        }
    } else {
        alert("灵力不足，无法外出历练！");
    }
}

function getNextRealm(currentRealm) {
    const realms = Object.keys(realmThresholds);
    const currentIndex = realms.indexOf(currentRealm);
    if (currentIndex !== -1 && currentIndex < realms.length - 1) {
        return realms[currentIndex + 1];
    }
    return null;
}

function realmUpgrade() {
    const nextRealm = getNextRealm(playerData.realm);
    if (nextRealm) {
        const threshold = realmThresholds[nextRealm];
        if (playerData.spirit >= threshold) {
            // 计算突破失败概率
            const failureChance = getFailureChance(nextRealm);
            if (Math.random() < failureChance) {
                // 突破失败
                playerData.spirit = 0;
                updateUI();
                savePlayerData();
                alert(`很遗憾，突破到${nextRealm}境界失败，灵力消耗殆尽！`);
            } else {
                // 突破成功
                playerData.spirit = 0;
                playerData.realm = nextRealm;
                onRealmUpgrade(playerData.realm); // 触发自动增加灵力的效果
                updateUI();
                savePlayerData();
                alert(`恭喜你突破到了${nextRealm}境界！`);
            }
        } else {
            alert(`灵力不足，突破到${nextRealm}境界需要${threshold}灵力！`);
        }
    } else {
        alert("你已达到最高境界！");
    }
}

function getFailureChance(nextRealm) {
    const realms = Object.keys(realmThresholds);
    const currentIndex = realms.indexOf(nextRealm);
    if (currentIndex !== -1) {
        // 失败概率随境界递增
        return (currentIndex + 1) * 0.1; // 假设每高一境界，失败概率增加10%
    }
    return 0;
}

function openShop() {
    document.getElementById("gamePanel").style.display = "none";
    document.getElementById("shop").style.display = "block";
}

function closeShop() {
    document.getElementById("gamePanel").style.display = "block";
    document.getElementById("shop").style.display = "none";
}

function buyItem(itemName, price) {
    if (playerData.currency >= price) {
        playerData.currency -= price;

        // 检查玩家背包中是否已经有同类型的装备，如果有则替换；如果没有则添加到空槽位
        if (itemName === "剑") {
            if (playerData.equipment1 === "无") {
                playerData.equipment1 = itemName;
                playerData.durability1 = 5; // 设置剑的初始耐久度为5
            } else if (playerData.equipment2 === "无") {
                playerData.equipment2 = itemName;
                playerData.durability2 = 5; // 设置剑的初始耐久度为5
            } else {
                // 替换装备1的剑
                playerData.equipment1 = itemName;
                playerData.durability1 = 5; // 设置剑的初始耐久度为5
            }
        } else if (itemName === "药") {
            if (playerData.equipment1 === "无") {
                playerData.equipment1 = itemName;
            } else if (playerData.equipment2 === "无") {
                playerData.equipment2 = itemName;
            } else {
                // 替换装备1的药
                playerData.equipment1 = itemName;
            }
        }

        updateUI();
        savePlayerData();
        alert(`购买成功！你获得了${itemName}`);
    } else {
        alert("灵石不足，购买失败！");
    }
}

// 初始化游戏
loadPlayerData();
updateUI();
