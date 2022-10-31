<script>
  import { BarChartSimple } from '@carbon/charts-svelte';
  import '@carbon/styles/css/styles.css';
  import '@carbon/charts/styles.css';
  import axios from 'axios';

  let data = [];

  async function GetKeywordRanking() {
    try {
      const response = await axios.get(`http://localhost:8000/analysis/top-freq-keywords`);

      if (response.data) {
        data = response.data;
      }
    } catch (error) {
      console.log(error);
    }
  }

  $: GetKeywordRanking();
</script>

<BarChartSimple
  {data}
  options={{
    title: 'Top 10 keywords',
    axes: {
      left: {
        mapsTo: 'group',
        scaleType: 'labels'
      },
      bottom: {
        mapsTo: 'value'
      }
    },
    height: '400px'
  }}
/>
