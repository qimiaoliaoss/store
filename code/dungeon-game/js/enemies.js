// enemies.js
export function generateEnemy(floor) {
    const enemies = [
        {
            name: '哥布林',
            hp: Math.floor(20 + floor * 3),
            attack: 5 + Math.floor(floor * 0.5),
            defense: 2 + Math.floor(floor * 0.3),
            gold: 10 + floor * 2,
            type: 'combat'
        },
        {
            name: '骷髅战士',
            hp: 35 + floor * 4,
            attack: 8 + floor * 0.7,
            defense: 4 + Math.floor(floor * 0.5),
            gold: 15 + floor * 3,
            type: 'combat'
        }
    ];

    // 每5层出现boss
    if (floor % 5 === 0) {
        return {
            name: `层主·魔龙（第${floor}层）`,
            hp: 100 + floor * 10,
            attack: 15 + floor,
            defense: 8 + Math.floor(floor * 0.8),
            gold: 50 + floor * 5,
            type: 'boss'
        };
    }

    return enemies[Math.floor(Math.random() * enemies.length)];
}
