// 定义怪物和玩家的初始状态
let monsters = [
  {
    name: 'Goblin',
    health: 50,
    mana: 20,
    defense: 5,
    damage: 8,
    skills: [
      {
        name: 'Stab',
        effect: function () {
          return this.damage; // Stab skill simply deals extra damage
        },
      },
      {
        name: 'Stealth',
        effect: function () {
          return Math.random() < 0.5 ? this.damage * 2 : 0; // 50% chance to deal double damage
        },
      },
    ],
  },
  {
    name: 'Orc',
    health: 80,
    mana: 10,
    defense: 8,
    damage: 12,
    skills: [
      {
        name: 'Smash',
        effect: function () {
          return this.damage + 5; // Smash skill deals extra damage
        },
      },
      {
        name: 'Roar',
        effect: function () {
          return 0; // Roar skill doesn't deal direct damage
        },
      },
    ],
  },
  {
    name: 'Dragon',
    health: 150,
    mana: 50,
    defense: 15,
    damage: 20,
    skills: [
      {
        name: 'Fire Breath',
        effect: function () {
          return this.damage * 1.5; // Fire Breath deals 1.5 times damage
        },
      },
      {
        name: 'Tail Swipe',
        effect: function () {
          return this.damage + 10; // Tail Swipe deals extra damage
        },
      },
    ],
  },
];

let player = {
  health: 100,
  mana: 30,
  defense: 10,
  damage: 15,
  skills: [
    {
      name: 'Attack',
      effect: function () {
        return this.damage; // Basic attack
      },
    },
    {
      name: 'Heal',
      effect: function () {
        const healAmount = 20;
        this.health = Math.min(100, this.health + healAmount); // Heal for 20 health points
        return healAmount;
      },
    },
  ],
  inventory: [],
};

// 当前遇到的怪物
let currentMonster = null;

// 更新游戏状态的函数
function updateGame() {
  document.getElementById('monster-container').innerHTML = `
    <p>怪物: ${currentMonster.name}</p>
    <p>生命值: ${currentMonster.health}</p>
    <p>法力值: ${currentMonster.mana}</p>
    <p>防御力: ${currentMonster.defense}</p>
    <p>攻击力: ${currentMonster.damage}</p>
    <p>技能: ${currentMonster.skills.map(skill => skill.name).join(', ')}</p>
  `;

  document.getElementById('player-container').innerHTML = `
    <p>玩家生命值: ${player.health}</p>
    <p>玩家法力值: ${player.mana}</p>
    <p>玩家防御力: ${player.defense}</p>
    <p>玩家攻击力: ${player.damage}</p>
    <p>玩家技能: ${player.skills.map(skill => skill.name).join(', ')}</p>
    <p>背包: ${player.inventory.join(', ')}</p>
  `;
}

// 开始遇到新怪物
function encounterMonster() {
  // 从怪物数组中随机选择一个怪物
  currentMonster = monsters[Math.floor(Math.random() * monsters.length)];

  // 更新游戏状态
  updateGame();

  alert(`一只${currentMonster.name}出现了！准备战斗吧！`);
}

// 攻击函数
function attack() {
  // 玩家使用一个随机的技能
  const playerSkill = player.skills[Math.floor(Math.random() * player.skills.length)];
  const playerDamage = playerSkill.effect.call(player);

  // 怪物使用一个随机的技能
  const monsterSkill = currentMonster.skills[Math.floor(Math.random() * currentMonster.skills.length)];
  const monsterDamage = monsterSkill.effect.call(currentMonster);

  // 对怪物和玩家应用伤害
  currentMonster.health -= playerDamage;
  player.health -= Math.max(0, monsterDamage - player.defense);

  // 更新游戏状态
  updateGame();

  // 检查游戏是否结束
  checkGameOver();
}

// 收集战利品函数
function collectLoot() {
  // 模拟随机掉落的装备物品
  const lootTypes = ['剑', '药水'];
  const randomLootType = lootTypes[Math.floor(Math.random() * lootTypes.length)];

  // 根据掉落类型执行相应的操作
  switch (randomLootType) {
    case '剑':
      // 获得剑，增加玩家的攻击力
      const swordDamageBonus = 5;
      player.damage += swordDamageBonus;
      alert(`你找到了一把剑！你的攻击力增加了${swordDamageBonus}点。`);
      break;
    case '药水':
      // 获得药水，恢复玩家的生命值
      const potionHealAmount = 30;
      player.health = Math.min(100, player.health + potionHealAmount);
      alert(`你找到了一瓶治疗药水！你的生命值恢复了${potionHealAmount}点。`);
      break;
    // 可以添加更多的战利品类型和效果
  }

  // 更新游戏状态
  updateGame();
}

// 检查游戏是否结束
function checkGameOver() {
  if (currentMonster.health <= 0) {
    alert(`你战胜了${currentMonster.name}！胜利！`);

    // 移动收集战利品的逻辑到战胜怪物后
    collectLoot();

    encounterMonster();
  } else if (player.health <= 0) {
    alert('游戏结束！怪物战胜了你。');
    resetGame();
  }
}

// 重置游戏
function resetGame() {
  player.health = 100;
  player.mana = 30;
  player.defense = 10;
  player.damage = 15;
  player.skills = [
    {
      name: '攻击',
      effect: function () {
        return this.damage; // 基础攻击
      },
    },
    {
      name: '治疗',
      effect: function () {
        const healAmount = 20;
        this.health = Math.min(100, this.health + healAmount); // 治疗 20 点生命值
        return healAmount;
      },
    },
  ];
  player.inventory = [];

  currentMonster = null;

  alert('游戏重置。开始新的冒险！');
  encounterMonster();
}

// 初始化游戏
resetGame();