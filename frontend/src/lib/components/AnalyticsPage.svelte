<script lang="ts">
  import { Grid, Row, Column } from 'carbon-components-svelte';
  import { MultiSelect, Dropdown, Select, SelectItem } from 'carbon-components-svelte';
  import axios from 'axios';
  // import Grid from 'svelte-grid';
  // import gridHelp from 'svelte-grid/build/helper/index.mjs';

  // const { item } = gridHelp;
  // const id = () => '_' + Math.random().toString(36).substr(2, 9);

  // let items = [
  //   {
  //     id: id(),
  //     5: item({
  //       x: 0,
  //       y: 0,
  //       w: 2,
  //       h: 2
  //     }),
  //     3: item({ x: 0, w: 2, h: 2, y: 0 }),
  //     1: item({ x: 0, y: 0, w: 1, h: 2 })
  //   },
  //   {
  //     id: id(),
  //     5: item({
  //       x: 2,
  //       y: 0,
  //       w: 3,
  //       h: 2
  //     }),
  //     3: item({ x: 2, w: 1, h: 2, y: 0 }),
  //     1: item({ x: 0, y: 2, w: 1, h: 2 })
  //   },

  //   {
  //     id: id(),
  //     5: item({
  //       x: 0,
  //       y: 2,
  //       w: 5,
  //       h: 2
  //     }),
  //     3: item({ x: 0, w: 3, h: 2, y: 2 }),
  //     1: item({ x: 0, y: 4, w: 1, h: 2 })
  //   }
  // ];

  // const cols = [
  //   [1500, 5],
  //   [1024, 3],
  //   [500, 1]
  // ];

  //CONTENT TOP MENU > SAVE / CANCEL BUTTONS ETC
  import { Tile, Button } from 'carbon-components-svelte';
  import Save from '~icons/bx/save';

  //CHARTS
  import WordCloud from '../components/charts/WordCloud.svelte';
  import Donut from '../components/charts/Donut.svelte';
  import HorizontalBar from '../components/charts/HorizontalBar.svelte';

  let caller_items = [
    { id: '0', text: 'Operator & Caller' },
    { id: '1', text: 'Operator' },
    { id: '2', text: 'Caller' }
  ];

  let type_items = [];
  let barChartData = [];
  let wordCloudData = [];
  let barchart_selectedId = '0';
  let wordcloud_selectedId = [];

  // dropdown (bar chart)
  const formatSelected = (id) => caller_items.find((item) => item.id === id)?.text ?? 'N/A';

  // multi-select (word cloud)
  const formatSelectedId = (i) =>
    i.length === 0 ? '0' : i.map((id) => type_items.find((item) => item.id === id).id).join(', ');

  const formatSelectedText = (i) =>
    i.length === 0
      ? 'N/A'
      : i.map((id) => type_items.find((item) => item.id === id).text).join(', ');

  $: barChartText = formatSelected(barchart_selectedId);
  $: wordCloudId = formatSelectedId(wordcloud_selectedId);
  $: wordCloudText = formatSelectedText(wordcloud_selectedId);

  async function GetKeywordExtraction(filter) {
    try {
      const response = await axios.get(`http://localhost:8000/analysis/own-keyword-extraction`);

      if (response.data) {
        // default
        if (filter == 'N/A') {
          wordCloudData = response.data;
        }
        // both Fire and Medical
        else if (filter.includes('Fire') && filter.includes('Medical')) {
          wordCloudData = response.data.filter(
            (kw) => kw.group.includes('Fire') && kw.group.includes('Medical')
          );
        }
        // Fire or Medical
        else {
          wordCloudData = response.data.filter((kw) => kw.group == filter);
        }
      }
    } catch (error) {
      console.log(error);
    }
  }

  async function GetKeywordRanking(filter) {
    try {
      // operator
      if (filter == 'Operator') {
        const response = await axios.get(`http://localhost:8000/analysis/top-operator-keywords`);
        if (response.data) {
          barChartData = response.data;
        }
      }
      // caller
      else if (filter == 'Caller') {
        const response = await axios.get(`http://localhost:8000/analysis/top-caller-keywords`);
        if (response.data) {
          barChartData = response.data;
        }
      } else {
        // default - both operator/caller
        const response = await axios.get(`http://localhost:8000/analysis/top-freq-keywords`);
        if (response.data) {
          barChartData = response.data;
        }
      }
    } catch (error) {
      console.log(error);
    }
  }

  async function GetTypes() {
    try {
      const response = await axios.get(`http://localhost:8000/analysis/get-types`);

      if (response.data) {
        // for (var i = 0; i < response.data.length; i++) {
        //   items.push(response.data[i]);
        // }
        type_items = response.data;
      }
    } catch (error) {
      console.log(error);
    }
  }

  $: GetKeywordRanking(barChartText);
  $: GetKeywordExtraction(wordCloudText);
  $: GetTypes();
</script>

<!-- CONTENT TOP MENU > SAVE / CANCEL BUTTONS ETC -->
<Tile class="!flex items-center">
  <h3>Analytics</h3>
  <Button icon={Save} size="small" class="!mx-2">Save</Button>
</Tile>
<!-- <div class="h-[80vh] overflow-auto p-4 m-6">
  <div class="demo-container size">
    <Grid bind:items rowHeight={100} let:item {cols} let:index>
      <div class="demo-widget content">
        <h3>{index}</h3>
      </div>
    </Grid>
  </div>
</div> -->

<br />

<div class="container mx-auto pl-10 pr-20">
  <div class="grid grid-cols-3 gap-4">
    <div class="...">
      <MultiSelect titleText="Top Keywords Filter - Type" label="Select types..." />
    </div>
    <div class="...">
      <!-- Sorted by 5/10/15/20 etc -->
      <MultiSelect titleText="Top Keywords Filter - Number" label="Select number..." />
    </div>
    <div class="...">
      <Dropdown
        titleText="Top Keywords Filter - Operator/Caller"
        bind:selectedId={barchart_selectedId}
        bind:items={caller_items}
      />
    </div>
    <div>Primary: {barChartText}</div>
  </div>
  <br />
  <section class="bg-slate-50 rounded-xl p-5 h-fit">
    <HorizontalBar {barChartData} />
  </section>
  <br />
  <div class="grid grid-cols-3 gap-4">
    <div class="col-span-2 ...">
      <MultiSelect
        titleText="Word Cloud Filter"
        bind:selectedIds={wordcloud_selectedId}
        label="Select types..."
        bind:items={type_items}
      />
      <br />
      <section class="bg-slate-50 rounded-xl p-5 h-fit">
        <WordCloud {wordCloudData} />
      </section>
    </div>
    <div class="...">
      <MultiSelect titleText="Donut Filter" label="Select types..." />
      <br />
      <section class="bg-slate-50 rounded-xl p-5 h-fit">
        <Donut />
      </section>
    </div>
  </div>
  <br />
</div>

<!-- <style>
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
</style> -->
