<template>
  <div class="w-screen h-screen box-border flex">
    <SidebarMenu class="flex-none" />
    <div class="flex-auto overflow-y-auto overscroll-none">
      <router-view />
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import SidebarMenu from '@/components/SidebarMenu/index.vue'
import useDataLakeStore from '../stores/data-lake'

const lakeStore = useDataLakeStore()

onMounted(() => {
  lakeStore.fetchGroupList('t')
  lakeStore.fetchGroupList('s')
  lakeStore.fetchGroupList('p')
})
</script>
