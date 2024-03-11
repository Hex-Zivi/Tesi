let replace = false;
let url = "";

function setTable(first_child){
    let div_tables = [];
    let tables = Array.from(document.getElementsByTagName("table"));
    let search_inputs = [];
    let paginates = [];

    let somma = 0;
    let index_css = []

    tables.forEach((table, index) => {
        div_tables[index] = document.getElementById(table.getAttribute("id") + "_wrapper");
        search_inputs[index] = document.getElementById(table.getAttribute("id") +"_filter")
        paginates[index] = document.getElementById(table.getAttribute("id") +"_paginate")
        for (let i = 0; i < (document.styleSheets[2].cssRules.length); i++){
            if (document.styleSheets[2].cssRules[i].cssText.includes("#" + table.id + "_wrapper::-webkit-scrollbar-track") || document.styleSheets[2].cssRules[i].cssText.includes("#" + table.id + "_wrapper::-webkit-scrollbar-thumb")){
                index_css.push(i)
            }
        }
    });

    index_css.forEach(() =>{
        document.styleSheets[2].deleteRule(0);
    })

    //set left search input
    search_inputs.forEach((search_input, index) =>{
        if (search_input){
            search_input.style.left = (div_tables[index].clientWidth - search_input.clientWidth) + "px";
            search_input.style.visibility = "visible";
        }
    })

    paginates.forEach((paginate, index) => {
        if (paginate){
            paginate.style.left = (div_tables[index].clientWidth - paginate.clientWidth) + "px";
            paginate.style.visibility = "visible";
        }
    })

    //set left th e td table
    tables.forEach((table, index) => {
        somma = 0;
        let empty = 10;
        if (table && div_tables[index]){
            if (table.clientWidth > div_tables[index].clientWidth){
                let ths = document.querySelectorAll("#" + table.id + " thead th:nth-child(-n + " + first_child + ")");
                let tds = document.querySelectorAll("#" + table.id + " tbody td:nth-child(-n + " + first_child + ")");
                if(tds[0].getAttribute("class") === "dataTables_empty"){
                    if (ths){
                        for (let i = 0; i < ths.length; i++ ){
                            ths[i].style.position = "unset"
                            ths[i].style.left = "0";
                            div_tables[index].style.paddingBottom = 22 + "px"
                            empty = 0
                            somma = 0
                        }
                    }
                }else{
                    if (ths && tds){
                        for (let i = 0; i < ths.length; i++ ){
                            ths[i].style.position = "sticky"
                            ths[i].style.left = somma + "px";
                            somma += Math.ceil(ths[i].clientWidth);
                        }

                        somma = 0;

                        for (let i = 0; i < tds.length && i < tds.length; i++){

                            tds[i].style.left = somma + "px";
                            somma += Math.ceil(tds[i].clientWidth);
                            if((i + 1) % first_child === 0 && i+1 !== tds.length){
                                somma = 0;
                            }
                        }

                    }
                }
            }else{
                let ths = document.querySelectorAll("#" + table.id + " thead th:nth-child(-n + " + first_child + ")");
                let tds = document.querySelectorAll("#" + table.id + " tbody td:nth-child(-n + " + first_child + ")");
                if(tds[0].getAttribute("class") === "dataTables_empty"){
                    if (ths){
                        for (let i = 0; i < ths.length; i++ ){
                            ths[i].style.position = "unset"
                            ths[i].style.left = "0";
                            div_tables[index].style.paddingBottom = 22 + "px"
                            empty = 0
                            somma = 0;
                        }
                    }
                }
            }
            document.styleSheets[2].addRule("#" + table.id + "_wrapper::-webkit-scrollbar-track", "margin-left: " + (somma + empty) + "px", 0);
            document.styleSheets[2].addRule("#" + table.id + "_wrapper::-webkit-scrollbar-track", "visibility: visible",1);
            document.styleSheets[2].addRule("#" + table.id + "_wrapper::-webkit-scrollbar-thumb", "visibility: visible", 2);
        }
    });
}

function createMessage(dowload, data, ...args){
    let avviso = document.getElementById("avviso");
    let block_page = document.getElementById("block-page");

    avviso.style.display = "block";
    avviso.classList.add("avviso-animated");
    block_page.classList.add("block-page")

    if (dowload){
        $('.content-avviso').html("<p id='message' style='margin-bottom: 0'></p>" +
            "<button class='btn' onclick='hideMessage()' style='margin-bottom: 20px'>OK</button>" +
            "<form action='downloadFile' method='POST' style='text-align: center'>" +
            "<input name='fileName' type='hidden' value="+ args[0] +">" +
            " <p style='margin-bottom: 0'>Scarica file ESSE3 aggiornato:</p> " +
            "<input type='submit' value='Scarica' class='btn' style='margin-bottom: 20px'></form>" );
    }

    let message = ""

    if (typeof data != "string"){
        data.forEach(object => {
            message += "<p style='margin-bottom: 0'>" + object + "</p>"
        })
    }else{
        message = "<p>" + data + "</p>"
    }

    document.getElementById("message").innerHTML = message;
}

function hideMessage(){
    let avviso = document.getElementById("avviso");
    let block_page = document.getElementById("block-page");

    avviso.style.display = "none";
    avviso.classList.remove("avviso-animated");
    block_page.classList.remove("block-page");
    if (replace){
        window.location.replace($SCRIPT_ROOT + url)
    }else{
        window.location.reload(true)
    }

}