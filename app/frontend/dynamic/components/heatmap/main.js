import Heatmap from './Heatmap.svelte';

const app = Heatmap({
  target: document.getElementById('app'),
  props: {
    data: {}
  }
});
