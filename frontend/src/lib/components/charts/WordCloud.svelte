<script>
  import chartData from '../../data/wordcloudData.json';
  import { WordCloudChart } from '@carbon/charts-svelte';
  import '@carbon/styles/css/styles.css';
  import '@carbon/charts/styles.css';

  let data = chartData;
</script>

<WordCloudChart
  {data}
  options={{
    title: 'Word cloud',
    resizable: true,
    color: {
      pairing: {
        option: 3
      }
    },
    height: '400px'
  }}
/>
