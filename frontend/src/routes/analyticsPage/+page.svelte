<script lang="ts">
  import AnalyticsPage from "$lib/components/AnalyticsPage.svelte";

  //CONTENT TOP MENU > SAVE / CANCEL BUTTONS ETC
  import { Tile, Button } from "carbon-components-svelte"; 
  import Save from "~icons/bx/save"
</script>

<!-- CONTENT TOP MENU > SAVE / CANCEL BUTTONS ETC -->
<Tile class="!flex">
  <h3>Analytics</h3>
  <Button icon={Save} size="small" class="!mx-2">Save</Button>
</Tile>
<div class="h-[80vh] overflow-auto p-4 m-6">
  <AnalyticsPage />
</div>