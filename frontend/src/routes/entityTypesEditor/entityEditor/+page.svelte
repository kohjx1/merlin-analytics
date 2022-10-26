<script lang="ts">
  import Entities from "$lib/components/Entities.svelte";

  //CONTENT TOP MENU > SAVE / CANCEL BUTTONS ETC
  import { Tile, Button } from "carbon-components-svelte"; 
  import Save from "~icons/bx/save"
</script>

<!-- CONTENT TOP MENU > SAVE / CANCEL BUTTONS ETC -->
<Tile class="!flex items-center">
  <h3>Entity Type: </h3>
  <Button icon={Save} size="small" class="!mx-2">Save</Button>
</Tile>
<div class="h-[80vh] overflow-auto p-4 m-6">
  <Entities />
</div>