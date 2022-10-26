<script lang="ts">
  import FormEditor from "$lib/components/FormListTable.svelte";

  //CONTENT TOP MENU > SAVE / CANCEL BUTTONS ETC
  import { Tile, Button } from "carbon-components-svelte"; 
  import Add from "~icons/carbon/add"
</script>

<!-- CONTENT TOP MENU > SAVE / CANCEL BUTTONS ETC -->
<Tile class="!flex items-center">
  <h3>Forms</h3>
  <Button icon={Add} size="small" class="!mx-2">New</Button>
</Tile>
<div class="h-[80vh] overflow-auto p-4 m-6">
  <FormEditor />
</div>