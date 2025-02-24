// events.js
import { generateEnemy } from './enemies.js';
import {logEvent} from "./ui.js";
export function handleRandomEvent(player) {
    const eventTypes = [
        { type: 'combat', weight: 60 },
        { type: 'treasure', weight: 25 },
        { type: 'trap', weight: 15 }
    ];

    const totalWeight = eventTypes.reduce((sum, e) => sum + e.weight, 0);
    let random = Math.random() * totalWeight;

    let selectedEvent;
    for (const event of eventTypes) {
        random -= event.weight;
        if (random <= 0) {
            selectedEvent = event.type;
            break;
        }
    }

    switch(selectedEvent) {
        case 'combat':
            const enemy = generateEnemy(player.floor);
            logEvent(player, `遭遇 ${enemy.name}！`);
            return {
                type: 'combat',
                enemy: enemy,
                description: '遭遇了凶猛的敌人！'
            };

        case 'treasure':
            const gold = 20 + Math.floor(Math.random() * player.floor * 5);
            player.addGold(gold);
            return {
                type: 'treasure',
                gold: gold,
                description: `发现了宝箱！获得${gold}金币`
            };

        case 'trap':
            const damage = 10 + Math.floor(Math.random() * 5);
            player.takeDamage(damage);
            return {
                type: 'trap',
                damage: damage,
                description: `触发陷阱，受到${damage}点伤害`
            };
    }
}
