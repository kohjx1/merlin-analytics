<script>
    import { Grid, Row, Column } from 'carbon-components-svelte';
    import { ClickableTile } from 'carbon-components-svelte';

    export let agents;
    const localAgents = agents.map((agent) => agent);
    $: changeArray(localAgents)

    let twoDArray = [];
    function changeArray(agents) {   //Change to rows of 3
        let oneDArray = agents;
        let remainder = oneDArray.length%3;
        while(oneDArray.length) 
            twoDArray.push(oneDArray.splice(0,3));
        //PUSH empty strings to fill up
        if(twoDArray[twoDArray.length-1]) {
            if(remainder === 2)     //PUSH 1
                twoDArray[twoDArray.length-1].push('');
            else if (remainder === 1) { //PUSH 2
                twoDArray[twoDArray.length-1].push('');
                twoDArray[twoDArray.length-1].push('');
            }
        }
        // console.log(twoDArray[twoDArray.length-1])
    }

    function switchAgent(agent) {
        // console.log(agent);
        selectedAgent = agent
    }

    export let selectedAgent = "";
</script>

<Grid padding class="!pr-20">
    {#each twoDArray as row, i}
        <Row>
            {#each row as cell, j}
                <Column>
                    {#if cell !== ''}
                        <ClickableTile class="!p-20 text-center" href="/" on:click={() => {switchAgent(cell)}}>
                            {cell}
                        </ClickableTile>
                    {/if}
                </Column>
            {/each}
        </Row>
    {/each}
</Grid>
