<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
/** * 如果不需要逻辑，script 标签可以保持简洁 
 * 但为了符合规范，我们可以留一个空的 setup 
 */
</script>

<style>
/* 基础全局样式，防止页面有白边 */
html, body, #app {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  background-color: #f5f7fa;
}
</style>