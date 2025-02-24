import { generateEnemy } from './enemies.js';
import {logEvent} from "./ui.js";

export class CombatSystem {
    static calculateDamage(attacker, defender) {
        return Math.max(0, attacker.attack - Math.floor(defender.defense / 2));
    }

    static performBattle(player, enemy) {
        logEvent(player, `与${enemy.name}交战开始`);
        const playerDamage = this.calculateDamage(player, enemy);
        const enemyDamage = this.calculateDamage(enemy, player);

        while (enemy.hp > 0 && player.currentHp > 0) {
            enemy.hp -= playerDamage;
            logEvent(player, `造成${playerDamage}点伤害`);
            if (enemy.hp <= 0) break;
            player.takeDamage(enemyDamage);
            logEvent(player, `受到${enemyDamage}点伤害`);
        }
    }
}
