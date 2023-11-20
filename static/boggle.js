class BoggleGame {
    constructor(boardId, secs=60){
        this.secs = secs;
        this.showTimer();

        this.score = 0;
        this.words = new Set();
        this.board = ('#' + boardId);

        //every second, async tick()
        this.timer = setInterval(this.tick.bind(this), 1000);

        $(".add-word", this.board).on("submit", this.handleAddWord.bind(this));
    }
    showMessage(msg, cls){
        $(".msg", this.board).text(msg).removeClass().addClass(`msg ${cls}`);
    }
    showWord(word){
        $(".words", this.board).append($("<li>", { text: word }));
    }
    showScore(){
        $(".score", this.board).text(this.score);
    }
    async handleAddWord(evt){
        evt.preventDefault();
        const $word = $(".word",this.board);
        let word = $word.val();
        if(!word) return;
        if (this.words.has(word)){
            this.showMessage(`already has ${word}`,"err")
            return;
        } 
        const resp = await axios.get("/check-word", {params: {word: word}});
        if (resp.data.result == "not-word"){
            this.showMessage(`${word} is not a valid word`, "err");
        } else if (resp.data.result == "not-on-board"){
            this.showMessage(`${word} in not a word on this board`);
        } else {
            this.showWord(word);
            this.score +=word.length;
            this.showScore();
            this.words.add(word);
            this.showMessage(`added ${word}`, "ok");
        }
        $word.val("").focus();
    }
    
    async postScore(){
        $(".add-word",this.board).hide();
        //sent score and get 
        const resp = await axios.post("/post-score", {score: this.score});
        // if score>highscore is True
        if (resp.data.brokeRecord) {
            this.showMessage(`New Record: ${this.score}`, "ok");
        } else {
            this.showMessage(`Your final score: ${this.score}, "ok"`);
        }
    }

    showTimer(){
        $(".timer", this.board).text(this.secs);
    }

    async tick(){
        this.secs -= 1;
        this.showTimer();
        if (this.secs == 0){
            clearInterval(this.timer);
            await this.postScore();
        }
    }
}

