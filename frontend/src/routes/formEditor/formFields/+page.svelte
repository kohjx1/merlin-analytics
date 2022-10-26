<script lang="ts">
  import DragNDropForm from '$lib/components/FormFieldsDragNDrop.svelte';

  //CONTENT TOP MENU > SAVE / CANCEL BUTTONS ETC
  import { Tile, Button } from 'carbon-components-svelte';
  import Save from '~icons/bx/save';
</script>

<!-- CONTENT TOP MENU > SAVE / CANCEL BUTTONS ETC -->
<Tile class="!flex items-center">
  <h3>Form Fields Editor</h3>
  <Button icon={Save} size="small" class="!mx-2">Save</Button>
</Tile>
<div class="h-[80vh] overflow-auto p-4 m-6">
  <DragNDropForm />
</div>
