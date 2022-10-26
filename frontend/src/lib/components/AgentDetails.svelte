<script>
  import { FluidForm, TextInput, Tile, Select, SelectItem, Button } from 'carbon-components-svelte';
  import { onMount, beforeUpdate } from 'svelte';

  import { agentDetail } from '$lib/stores';
  export let localAgentDetail = Object.assign({}, $agentDetail); //REASSIGN TO PREVENT THE BELOW
  export let newAgentDetail = Object.assign({}, $agentDetail); //REASSIGN TO PREVENT THE BELOW
  //$agentDetail GETS OVERWRITTEN BY when doing edits > to make sure does not happen with future API call onMount (should re-grab from DBafter re-mount)
  onMount(() => {
    // localAgentDetail = Object.assign({}, $agentDetail);
    // newAgentDetail = Object.assign({}, $agentDetail);
  });
  beforeUpdate(() => {
    if (JSON.stringify(localAgentDetail) !== JSON.stringify($agentDetail)) {
      localAgentDetail = Object.assign({}, $agentDetail);
      newAgentDetail = Object.assign({}, $agentDetail);
    }
  });
  
  //FOR DISABLING/ENABLING OF SAVE BUTTON
  let invalidInput = false;
  $: validateInput(newAgentDetail); //CHECK FOR EMPTY
  function validateInput() {
    if(newAgentDetail && newAgentDetail.name !== undefined) {
      invalidInput = /^$/.test(newAgentDetail.name);
    } else
      invalidInput = false;
  }
  //TODO: CHECK FOR DUPLICATE NAME

  let saveDisabledNoChanges = true;
  $: checkForChanges(newAgentDetail)

  function checkForChanges(newAgentDetail) {
    if (JSON.stringify(newAgentDetail) !== JSON.stringify(localAgentDetail)) {
      //IF CONTAINS INVALID INPUT --- DON'T ENABLE THE SAVE
      if(invalidInput)
        saveDisabledNoChanges = true;
      else
        saveDisabledNoChanges = false;
    }
    else 
      saveDisabledNoChanges = true;
  }

  //PREP COUNTRIES DATA
  // import { countries } from '$lib/countriesData.js';
  import countries from "$lib/data/countriesData.json";
  let countriesList = [];
  function changeStringCountry() {
    countries.forEach((country) => {
      countriesList.push(country.Name + ' (' + country.Code + ')');
    });
  }
  changeStringCountry();
  //PREP TIMEZONE DATA AND HANDLING FUNCTIONS
  import TimezonePicker from 'svelte-timezone-picker';
  let timezone = localAgentDetail.timezone;
  function update(ev) {
    newAgentDetail.timezone = ev.detail.timezone;
  }
  //PREP LANGUAGES DATA
  // import { languages } from '$lib/languagesData.js';
  import languages from "$lib/data/languagesData.json";
  let languagesList = [];
  function changeStringLanguage() {
    languages.forEach((language) => {
      languagesList.push(language.alpha2 + ' - ' + language.English);
    });
  }
  changeStringLanguage();

  //BUTTONS
  import Save from '~icons/bx/save';
  function saveAgentDetails() {
    console.log('SENDING TO DB: ' + JSON.stringify(newAgentDetail));
    //TODO - API CALL HERE

  }
</script>

<div class="h-[80vh] overflow-auto p-4 m-6 pr-20">
  <FluidForm>
    <TextInput
      labelText="Agent name"
      placeholder="Enter a name..."
      required
      invalid={invalidInput}
      invalidText="Name cannot be empty."
      bind:value={newAgentDetail.name}
    />
    <Select
      class="formSelect"
      labelText="Location"
      bind:selected={newAgentDetail.location}
      on:change={(e) => console.log('location value: ', e.detail)}
    >
      {#each countriesList as cty}
        <SelectItem value={cty} />
      {/each}
    </Select>
    <Tile class="border-b border-solid items-center" id="timepickerTile">
      <span class="manualLabel">Timezone</span>
      <TimezonePicker {timezone} on:update={update} />
    </Tile>
    <Select
      class="formSelect"
      labelText="Default language"
      bind:selected={newAgentDetail.lang}
      on:change={(e) => console.log('language value: ', e.detail)}
    >
      {#each languagesList as lang}
        <SelectItem value={lang} />
      {/each}
    </Select>
  </FluidForm>
  <Button
    disabled={saveDisabledNoChanges}
    icon={Save}
    class="!mt-2 float-right"
    on:click={() => {
      saveAgentDetails();
    }}>Save</Button
  >
  <div class="columns-2 mt-20 bg-gray-500/50">
    <pre>Before changes: <br />{JSON.stringify(localAgentDetail, null, 2)}</pre>
    <pre>After changes: <br />{JSON.stringify(newAgentDetail, null, 2)}</pre>
  </div>
</div>

<style>
  /* LIGHT THEME --- TimezonePicker */
  :root[theme='g10'] {
    --color-white: #fff;
    --color-info-900: #076196;
    --color-gray-100: rgba(0, 0, 0, 0.2);
    --color-gray-400: #acacac;
    --color-gray-600: #757575;
    --color-gray-900: #292929;
  }
  /* DARK THEME --- TimezonePicker */
  :root[theme='g80'] {
    --color-white: #525252;
    --color-info-900: #7aceff;
    --color-gray-100: rgba(0, 0, 0, 0.8);
    --color-gray-400: #acacac;
    --color-gray-600: #e8e8e8;
    --color-gray-900: #ffffff;
  }
  :global(#timepickerTile) {
    border-color: #a8a8a8 !important;
  }
  .manualLabel {
    font-size: var(--cds-label-01-font-size, 0.75rem);
    font-weight: var(--cds-label-01-font-weight, 400);
    line-height: var(--cds-label-01-line-height, 1.33333);
    letter-spacing: var(--cds-label-01-letter-spacing, 0.32px);
    display: inline-block;
    margin-bottom: 0.5rem;
    color: var(--cds-text-02, #525252);
    font-weight: 400;
    line-height: 1rem;
    vertical-align: baseline;
  }
  :global(.formSelect .bx--select-input) {
    min-height: 4rem;
    padding: 2rem 1rem 0.8125rem;
  }
</style>
