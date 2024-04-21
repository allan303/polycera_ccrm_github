<template>
  <div class="row">
    <div :class="genColClass({ s: 12, other: 'center-align' })">
      <h1>PAGE NOT FOUND : 404</h1>

      <h3 class="card-title">PolyCera<sup>&reg;</sup></h3>

      <h5 class="blue-text">
        <strong> BUG submit:</strong> Jack.li@polycera.com
      </h5>
      <div class="card-image">
        <img src="../../assets/polycera_skid.png" alt="没有图" />
      </div>
    </div>
  </div>
</template>
<script scope>
import { genColClass } from "@/myjs";

export default {
  setup() {
    return { genColClass };
  },
};
</script>
