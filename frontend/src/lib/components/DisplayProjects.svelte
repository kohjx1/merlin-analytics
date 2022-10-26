<script>
    import { Grid, Row, Column } from 'carbon-components-svelte';
    import { ClickableTile, Search } from 'carbon-components-svelte';
    import Add from '~icons/carbon/add';

    export let user = null;
    export let projects;
    let localProjects = projects.map((project) => project);
    $: changeArray(localProjects)

    let searchValue = "";
    $: updateArray(searchValue)

    function updateArray() {
        console.log("SEARCH VALUE: " + searchValue)
        // localProjects = projects.map((project) => project)
        changeArray()
    }

    let twoDArray = [];
    function changeArray(localArray) {   //Change to rows of 3
        let oneDArray = [];
        oneDArray = localProjects.map((project) => project)
        if(user.groups.includes("merlin-admin"))
        // if(user.groups.includes("merlin-user")) //FOR TESTING THAT IT DOESNT ADD
            oneDArray.push('Create New Project')
        //FILTER
        let filteredArray = [];
        if(searchValue !== "") {
            for (let i = oneDArray.length - 1; i >= 0; i--) {
                const element = oneDArray[i];
                if (element.toLowerCase().indexOf(searchValue.toLowerCase()) !== -1) {
                    filteredArray.push(element)
                }
            }
        } else 
            filteredArray = oneDArray;
        //SPLICE INTO 2D ARRAY
        twoDArray = [];
        let remainder = filteredArray.length%3;
        while(filteredArray.length) 
            twoDArray.push(filteredArray.splice(0,3));
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
        console.log(twoDArray)
    }

    function switchProject(project) {
        // console.log(project);
        selectedProject = project
    }

    export let selectedProject = "";
</script>

<div class="block m-auto mt-4 items-center w-1/3">
    <Search bind:value={searchValue} placeholder="Search Projects..."/>
</div>

<Grid padding class="!pr-20">
    {#each twoDArray as row, i}
        <Row>
            {#each row as cell, j}
                <Column>
                    {#if cell !== ''}
                        <ClickableTile class="!p-16 text-center" href="/" on:click={() => {switchProject(cell)}}>
                            {#if cell === "Create New Project"}
                                <Add width="50" height="50" class="block m-auto"/>
                                {cell}
                            {:else}
                                <!-- <div class="h-[25px]"></div> -->
                                <div class="py-[25px]">{cell}</div>
                                <!-- <div class="h-[25px]"></div> -->
                            {/if}
                        </ClickableTile>
                    {/if}
                </Column>
            {/each}
        </Row>
    {/each}
</Grid>
