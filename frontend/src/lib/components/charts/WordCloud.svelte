<script>
  import { WordCloudChart } from '@carbon/charts-svelte';
  import '@carbon/styles/css/styles.css';
  import '@carbon/charts/styles.css';

  export let wordCloudData = [];
</script>

<WordCloudChart
  data={wordCloudData}
  options={{
    title: 'Word cloud',
    resizable: true,
    color: {
      pairing: {
        option: 5
      }
    },
    height: '400px'
  }}
/>
