<template>
  <div class="flex items-center w-2/3">
    <SvgIcon name="Search" class="h-5 w-5" :strokeWidth="3" />
    <input
      :placeholder="placeholder"
      class="test-search-bar"
      v-model="query"
      @focus="clearSearchBar"
      @keyup.enter="pressedEnter"
    />
  </div>
</template>

<script setup lang="ts">
import { toRef } from 'vue'
import useTestsStore from '../../stores/test-list'

const placeholder = 'Search by test sequence'
const store = useTestsStore()

const query = toRef(store, 'query')

async function pressedEnter() {
  store.page = 1
  store.query = query.value
  await store.getTestList()
}

function clearSearchBar() {
  query.value = ''
}
</script>

<style>
@layer components {
  .test-search-bar {
    @apply bg-blue-100 rounded-lg h-9 w-full
    px-3 pt-2 pb-1 ml-2 focus:outline-none
    /* focus:ring focus:ring-blue-300 */
    hover:bg-blue-50
    focus:bg-blue-100;
  }
}
</style>
