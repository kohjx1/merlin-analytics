<script lang="ts">
  import Grid from 'svelte-grid';
  import gridHelp from 'svelte-grid/build/helper/index.mjs';

  const { item } = gridHelp;
  const id = () => '_' + Math.random().toString(36).substr(2, 9);

  let items = [
    {
      id: id(),
      5: item({
        x: 0,
        y: 0,
        w: 2,
        h: 2
      }),
      3: item({ x: 0, w: 2, h: 2, y: 0 }),
      1: item({ x: 0, y: 0, w: 1, h: 2 })
    },
    {
      id: id(),
      5: item({
        x: 2,
        y: 0,
        w: 3,
        h: 2
      }),
      3: item({ x: 2, w: 1, h: 2, y: 0 }),
      1: item({ x: 0, y: 2, w: 1, h: 2 })
    },

    {
      id: id(),
      5: item({
        x: 0,
        y: 2,
        w: 5,
        h: 2
      }),
      3: item({ x: 0, w: 3, h: 2, y: 2 }),
      1: item({ x: 0, y: 4, w: 1, h: 2 })
    }
  ];

  const cols = [
    [1500, 5],
    [1024, 3],
    [500, 1]
  ];

  //CONTENT TOP MENU > SAVE / CANCEL BUTTONS ETC
  import { Tile, Button } from "carbon-components-svelte"; 
  import Save from "~icons/bx/save"
</script>

<!-- CONTENT TOP MENU > SAVE / CANCEL BUTTONS ETC -->
<Tile class="!flex items-center">
  <h3>Analytics</h3>
  <Button icon={Save} size="small" class="!mx-2">Save</Button>
</Tile>
<div class="h-[80vh] overflow-auto p-4 m-6">
  <div class="demo-container size">
    <Grid bind:items rowHeight={100} let:item {cols} let:index>
      <div class="demo-widget content">
        <h3>{index}</h3>
      </div>
    </Grid>
  </div>
</div>

<style>
  .size {
    /* max-width: 1100px; */
    width: 100%;
  }
  .demo-widget {
    background: #f1f1f1;
    height: 100%;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .demo-container {
    /* max-width: 800px; */
    width: 100%;
  }
</style>
