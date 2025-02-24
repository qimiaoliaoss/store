import Player from './player.js';
import { CombatSystem } from './combat.js';
import { generateEnemy } from './enemies.js';
import { handleRandomEvent } from './events.js';
import {updateUI, logEvent, initUI} from './ui.js';

export default class Game {
    constructor() {
        this.player = new Player();
        this.isGameOver = false;
    }

    init() {
        initUI();
        updateUI(this.player);
        logEvent(this.player, "欢迎来到无尽地下城！");  // 传入player参数
        this.bindEvents();
    }

    bindEvents() {
        document.querySelector('#explore-btn').addEventListener('click', () => this.explore());
        document.querySelector('#shop-btn').addEventListener('click', () => this.shop());
    }

    explore() {
        if (this.isGameOver) return;

        // 处理随机事件
        const eventResult = handleRandomEvent(this.player);
        if (eventResult.type === 'combat') {
            CombatSystem.performBattle(this.player, eventResult.enemy);
            if (this.player.currentHp > 0) {
                this.player.addGold(eventResult.enemy.gold);
            }
        }

        this.player.floor++;
        this.checkGameOver();
        updateUI(this.player);
    }

    checkGameOver() {
        if (this.player.currentHp <= 0) {
            this.isGameOver = true;
            alert(`游戏结束！最高到达第${this.player.floor-1}层`);
        }
    }

    shop() {
        // 商店逻辑
    }
}
