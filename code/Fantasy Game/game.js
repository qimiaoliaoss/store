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
    <p>Monster: ${currentMonster.name}</p>
    <p>Health: ${currentMonster.health}</p>
    <p>Mana: ${currentMonster.mana}</p>
    <p>Defense: ${currentMonster.defense}</p>
    <p>Damage: ${currentMonster.damage}</p>
    <p>Skills: ${currentMonster.skills.map(skill => skill.name).join(', ')}</p>
  `;

  document.getElementById('player-container').innerHTML = `
    <p>Player Health: ${player.health}</p>
    <p>Player Mana: ${player.mana}</p>
    <p>Player Defense: ${player.defense}</p>
    <p>Player Damage: ${player.damage}</p>
    <p>Player Skills: ${player.skills.map(skill => skill.name).join(', ')}</p>
    <p>Inventory: ${player.inventory.join(', ')}</p>
  `;
}

// 开始遇到新怪物
function encounterMonster() {
  // 从怪物数组中随机选择一个怪物
  currentMonster = monsters[Math.floor(Math.random() * monsters.length)];

  // 更新游戏状态
  updateGame();

  alert(`A wild ${currentMonster.name} appears! Prepare for battle!`);
}

// 攻击函数
function attack() {
  // Player uses a random skill
  const playerSkill = player.skills[Math.floor(Math.random() * player.skills.length)];
  const playerDamage = playerSkill.effect.call(player);

  // Monster uses a random skill
  const monsterSkill = currentMonster.skills[Math.floor(Math.random() * currentMonster.skills.length)];
  const monsterDamage = monsterSkill.effect.call(currentMonster);

  // Apply damage to the monster and player
  currentMonster.health -= playerDamage;
  player.health -= Math.max(0, monsterDamage - player.defense);

  // Update game state
  updateGame();

  // Check if the game is over
  checkGameOver();
}

// 收集战利品函数
function collectLoot() {
  // 模拟随机掉落的装备物品
  const lootTypes = ['Sword', 'Potion'];
  const randomLootType = lootTypes[Math.floor(Math.random() * lootTypes.length)];

  // 根据掉落类型执行相应的操作
  switch (randomLootType) {
    case 'Sword':
      // 获得剑，增加玩家的攻击力
      const swordDamageBonus = 5;
      player.damage += swordDamageBonus;
      alert(`You found a Sword! Your damage increased by ${swordDamageBonus}.`);
      break;
    case 'Potion':
      // 获得药水，恢复玩家的生命值
      const potionHealAmount = 30;
      player.health = Math.min(100, player.health + potionHealAmount);
      alert(`You found a Healing Potion! Your health restored by ${potionHealAmount}.`);
      break;
    // 可以添加更多的战利品类型和效果
  }

  // 更新游戏状态
  updateGame();
}

// 检查游戏是否结束
function checkGameOver() {
  if (currentMonster.health <= 0) {
    alert(`You defeated the ${currentMonster.name}! Victory!`);

    // 移动收集战利品的逻辑到战胜怪物后
    collectLoot();

    encounterMonster();
  } else if (player.health <= 0) {
    alert('Game over! The monster defeated you.');
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
  ];
  player.inventory = [];

  currentMonster = null;

  alert('Game reset. Start a new adventure!');
  encounterMonster();
}

// 初始化游戏
resetGame();
