export default class Player {
    constructor() {
        this.floor = 1;
        this.maxHp = 100;
        this.currentHp = 100;
        this.attack = 10;
        this.defense = 5;
        this.gold = 0;
        this.inventory = [];
    }

    takeDamage(damage) {
        this.currentHp = Math.max(0, this.currentHp - damage);
    }

    heal(amount) {
        this.currentHp = Math.min(this.maxHp, this.currentHp + amount);
    }

    addGold(amount) {
        this.gold += amount;
    }
}
