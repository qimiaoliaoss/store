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
    "开化": 5, // 开化境每秒增加1点灵力
    "筋骨": 10, // 筋骨境每秒增加5点灵力
    "锻体": 50, // 锻体境每秒新增10点灵力
    "炼气": 100, // 炼气境每秒新增20点灵力
    "入窍": 200, // 入窍境每秒新增30点灵力
    "通神": 400, // 通神境每秒新增40点灵力
    "金丹": 2000, // 金丹境每秒新增50点灵力
    "元婴": 5000, // 元婴境每秒新增100点灵力
    "化神": 10000, // 化神境每秒新增150点灵力
};

const shopItems = [
    {
        name: "剑",
        type: "weapon", // 武器类型
        price: 10,
        description: "购买后增加剑的耐久度，剑的耐久度降低时消失。",
    },
    {
        name: "药",
        type: "item", // 道具类型
        price: 5,
        description: "购买后用于抵消外出历练失败时灵力清零的效果。",
    },
    {
        name: "秘笈残页",
        type: "book", // 道具类型
        price: 20,
        description: "购买后提高点击冥想时获得的灵力值5点。",
        spiritIncrease: 5,
    },
    {
        name: "秘笈残卷",
        type: "book", // 道具类型
        price: 50,
        description: "购买后提高点击冥想时获得的灵力值10点。",
        spiritIncrease: 10,
    },
  // 可以继续添加更多的商品信息
];

let playerData = {
    spirit: 0,
    currency: 0,
    equipment1: "无",
    equipment2: "无",
    durability1: 0,
    durability2: 0,
    realm: "凡人", // 设置默认境界为"凡人"
    // 添加用于记录购买秘笈数量的属性
    purchasedItems: {
        "秘笈残页": 0,
        "秘笈残卷": 0,
        // 可以根据需要添加更多秘笈
    },
    // 添加用于记录不同秘笈对灵力增加的效果
    spiritIncreases: {
        "秘笈残页": 0,
        "秘笈残卷": 0,
        // 可以根据需要添加更多秘笈
    },
    // 新增属性
    weaponSlot: null, // 记录武器栏中的武器
    itemsSlot: [], // 记录道具栏中的道具
    backpack: [], // 背囊，用于存放额外的道具和武器
};

function resetGame() {
    playerData = {
        spirit: 0,
        currency: 0,
        equipment1: "无",
        equipment2: "无",
        durability1: 0,
        durability2: 0,
        realm: "凡人", // 设置默认境界为"凡人"
        // 添加用于记录购买秘笈数量的属性
        purchasedItems: {
            "秘笈残页": 0,
            "秘笈残卷": 0,
            // 可以根据需要添加更多秘笈
        },
        // 添加用于记录不同秘笈对灵力增加的效果
        spiritIncreases: {
            "秘笈残页": 0,
            "秘笈残卷": 0,
            // 可以根据需要添加更多秘笈
        },
        // 新增属性
        weaponSlot: null, // 记录武器栏中的武器
        itemsSlot: [], // 记录道具栏中的道具
        backpack: [], // 背囊，用于存放额外的道具和武器
    };
    updateUI();
    savePlayerData();
}

// 突破到某个境界时的效果
function onRealmUpgrade(realm) {
    const spiritIncreaseSpeed = spiritIncreaseSpeeds[realm]; // 默认每秒增加20点灵力
    startAutoIncreaseSpirit(spiritIncreaseSpeed);
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


function updateUI() {
    document.getElementById("spirit").textContent = playerData.spirit;
    document.getElementById("currency").textContent = playerData.currency;
    // 更新武器栏
    const weaponSlotElement = document.getElementById("weaponSlot");
    weaponSlotElement.textContent = playerData.weaponSlot ? playerData.weaponSlot : "空";

    // 更新道具栏
    const itemsSlotElement = document.getElementById("itemsSlot");
    itemsSlotElement.textContent = playerData.itemsSlot.length > 0 ? playerData.itemsSlot.join(", ") : "空";

    // 更新背囊
    const backpackSlotElement = document.getElementById("backpackSlot");
    backpackSlotElement.textContent = playerData.backpack.length > 0 ? playerData.backpack.join(", ") : "空";
    document.getElementById("shopCurrency").textContent = playerData.currency;

    const nextRealm = getNextRealm(playerData.realm);
    onRealmUpgrade(playerData.realm);// 在加载玩家数据后重新设置自动增加灵力的效果
    document.getElementById("realm").textContent = playerData.realm;
    document.getElementById("nextRealmThreshold").textContent = nextRealm ? realmThresholds[nextRealm] : "已达最高境界";

}


function meditate() {
    // 增加基础灵力
    let totalSpiritIncrease = 1; // 基础冥想灵力增加为1

    // 累加购买的秘笈对灵力增加的效果
    for (const itemName in playerData.spiritIncreases) {
        totalSpiritIncrease += playerData.spiritIncreases[itemName];
    }

    playerData.spirit += totalSpiritIncrease; // 模拟冥想获得灵力
    updateUI();
    savePlayerData();
}

function outdoorTraining() {
    if (playerData.spirit > 0) {
        const consumedSpirit = Math.floor(Math.random() * playerData.spirit) + 1; // 消耗的灵力数量在1~当前灵力值之间
        const chance = Math.random(); // 外出历练的成功概率

        if (chance < 0.5) {
            if (consumedSpirit >= playerData.spirit) {
                handleFailedTraining();
            } else {
                handleSuccessfulTraining(consumedSpirit);
            }
        } else {
            alert("外出历练没有获得任何灵石。");
        }
    } else {
        alert("灵力不足，无法外出历练！");
    }
}

function handleFailedTraining() {
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
}

function handleSuccessfulTraining(consumedSpirit) {
    playerData.spirit -= consumedSpirit;

    let gainedCurrency = Math.floor(Math.random() * 6) + 5; // 获得的灵石数量在5~10之间

    // 检查玩家是否携带了“剑”道具，如果有则额外增加获得的灵石数量
    if (playerData.equipment1 === "剑" || playerData.equipment2 === "剑") {
        gainedCurrency += 5; // 剑增加额外的5个灵石
        // 剑的耐久度降低
        if (playerData.equipment1 === "剑") {
            playerData.durability1 -= 1;
        } else {
            playerData.durability2 -= 1;
        }
        // 检查剑的耐久度是否耗尽
        if (playerData.durability1 <= 0) {
            playerData.equipment1 = "无";
            playerData.durability1 = 0;
            alert("剑已损坏，需要重新购买。");
        }
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
                // playerData.spirit = 0;
                playerData.spirit = playerData.spirit - threshold;
                playerData.realm = nextRealm;
                updateUI();
                savePlayerData();
                alert(`恭喜你突破到了${nextRealm}境界！`);
                startAutoIncreaseSpirit(spiritIncreaseSpeeds[playerData.realm]); // 触发自动增加灵力的效果
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
        // 失败概率随境界递增，但不会超过50%
        return Math.min((currentIndex + 1) * 0.05, 0.5); // 假设每高一境界，失败概率增加5%，最大不超过50%
    }
    return 0;
}

function openShop() {
  document.getElementById("gamePanel").style.display = "none";
  document.getElementById("shop").style.display = "block";

  const shopItemsContainer = document.getElementById("shopItemsContainer");
  shopItemsContainer.innerHTML = ""; // 清空商店商品容器

  for (const item of shopItems) {
    const itemName = item.name;
    const price = item.price;
    const description = item.description;

    const itemDiv = document.createElement("div");
    itemDiv.classList.add("shopItem"); // 添加商品格子的样式类

    const itemButton = document.createElement("button");
    itemButton.textContent = `购买${itemName}(${price}灵石)`;
    itemButton.onclick = function () {
      buyItem(itemName, price);
    };
    itemDiv.appendChild(itemButton);

    const descriptionP = document.createElement("p");
    descriptionP.textContent = description;
    itemDiv.appendChild(descriptionP);

    shopItemsContainer.appendChild(itemDiv);
  }
}

function closeShop() {
    document.getElementById("gamePanel").style.display = "block";
    document.getElementById("shop").style.display = "none";
}

function buyItem(itemName, price) {
    if (playerData.currency >= price) {
        // 检查玩家是否已经购买过该秘笈五件
        const purchasedCount = playerData.purchasedItems[itemName];
        if (purchasedCount >= 5) {
            alert("你已经购买过该秘笈的最大数量！");
            return;
        }
        playerData.currency -= price;

        // 检查玩家背包中是否已经有同类型的装备或道具，如果有则放入背囊；如果没有则添加到空槽位
        const item = shopItems.find((item) => item.name === itemName);
        if (!item) {
            alert("道具不存在！");
            return;
        }

        if (item.type === "weapon") {
            if (playerData.weaponSlot === null) {
                playerData.weaponSlot = itemName;
                playerData.durability1 = 5; // 设置剑的初始耐久度为5
            } else {
                // 放入背囊
                playerData.backpack.push(itemName);
            }
        } else if (item.type === "item") {
            if (playerData.itemsSlot.length < 3) {
                playerData.itemsSlot.push(itemName);
            } else {
                // 放入背囊
                playerData.backpack.push(itemName);
            }
        }

        // 处理秘笈购买逻辑
        if (itemName === "秘笈残页" || itemName === "秘笈残卷") {
            const spiritIncrease = getItemSpiritIncrease(itemName);
            playerData.spiritIncreases[itemName] += spiritIncrease; // 累加购买的秘笈对灵力增加的效果
            // 增加玩家购买的秘笈数量
            playerData.purchasedItems[itemName] += 1;
        }

        updateUI();
        savePlayerData();
        alert(`购买成功！你获得了${itemName}`);
    } else {
        alert("灵石不足，购买失败！");
    }
}


function equipItem(itemName) {
    const item = shopItems.find((item) => item.name === itemName);
    if (!item) {
        alert("道具不存在！");
        return;
    }

    if (item.type === "weapon" && playerData.weaponSlot) {
        alert("武器栏已有武器装备，无法再装备剑！");
        return;
    }

    if (item.type === "item" && playerData.itemsSlot.length >= 3) {
        alert("道具栏已满，无法再装备道具！");
        return;
    }

    if (item.type === "weapon" && playerData.weaponSlot) {
        playerData.backpack.push(playerData.weaponSlot);
    } else if (item.type === "item" && playerData.itemsSlot.length >= 3) {
        playerData.backpack.push(playerData.itemsSlot.pop());
    }

    if (item.type === "weapon") {
        playerData.weaponSlot = itemName;
    } else {
        playerData.itemsSlot.push(itemName);
    }

    updateUI();
    savePlayerData();
}

function unequipItem(itemName) {
    const item = shopItems.find((item) => item.name === itemName);
    if (!item) {
        alert("道具不存在！");
        return;
    }

    if (item.type === "weapon" && !playerData.weaponSlot) {
        alert("武器栏没有装备剑！");
        return;
    } else if (item.type === "item" && !playerData.itemsSlot.includes(itemName)) {
        alert("道具栏没有装备该物品！");
        return;
    }

    if (item.type === "weapon") {
        playerData.weaponSlot = null;
    } else {
        playerData.itemsSlot = playerData.itemsSlot.filter((item) => item !== itemName);
    }

    updateUI();
    savePlayerData();
}

function getItemSpiritIncrease(itemName) {
    // 获取秘笈提供的灵力增加值
    for (const item of shopItems) {
        if (item.name === itemName && item.spiritIncrease) {
            return item.spiritIncrease;
        }
    }
    return 0;
}

// 初始化游戏
loadPlayerData();
updateUI();