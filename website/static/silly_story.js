function associate(lines, contextLen) {
    let words = {};
    let context = Array(contextLen).fill("");

    for(let line of lines){
        
        let tokens = line.trim().split(" ");
        tokens.push("\n");

        for(let token of tokens){
            let contextStr = context.join(" ");
            if (!words[contextStr]) words[contextStr] = [];
            words[contextStr].push(token);
            context = context.slice(1).concat([token]);
        }
    }
    
    return words;
}

function getContext(words, contextLen) {
    let context = Array(contextLen).fill("");
    let s = "";
  
    for (let i = 0; i < Object.keys(words).length - contextLen; i++) {
        let contextStr = context.join(" ");
        let wordList = words[contextStr] || [""];
        let word = wordList[Math.floor(Math.random() * wordList.length)];
        
        s += word === '\n' ? '\n' : `${word} `;
        
        context = context.slice(1).concat([word]);
    }
    
    return s.trim();
}
