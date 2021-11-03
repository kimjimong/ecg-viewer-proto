import { defineStore } from 'pinia'
import GroupApi from '../utils/group-api'
import useDataLakeStore from '../stores/data-lake'

const api = new GroupApi()

export interface TestChecked {
  [id: EcgTest.Id]: boolean
}

export interface PageChecked {
  [page: number]: boolean
}

export interface SampleChecked {
  [id: EcgTest.Id]: PageChecked
}

type GroupPageState = {
  type?: Resp.GroupType
  selectedGroupId?: number
  selectedGroupName?: string
  tests?: EcgTests
  samples?: [EcgTest.Meta, number[]][]
  checkedTestIds: TestChecked | SampleChecked
  loading: boolean
}

const useGroupPageStore = defineStore('groupPage', {
  state: () => {
    return {
      type: undefined,
      selectedGroupId: undefined,
      selectedGroupName: undefined,
      tests: [],
      samples: [],
      checkedTestIds: {},
      loading: false
    } as GroupPageState
  },
  actions: {
    resetGroupPage() {
      this.type = undefined
      this.selectedGroupId = undefined
      this.selectedGroupName = undefined
      this.tests = []
      this.samples = []
      this.checkedTestIds = {}
      this.loading = false
    },

    resetSelectedTestInfo() {
      this.selectedGroupId = undefined
      this.selectedGroupName = undefined
      this.tests = []
      this.samples = []
      this.checkedTestIds = {}
    },

    async fetchTestList(gid: number) {
      this.loading = true
      this.resetSelectedTestInfo()
      const res = await api.getTestsInGroup(this.type!, gid)
      if (res === undefined) return
      const lakeStore = useDataLakeStore()
      this.selectedGroupId = gid
      if (this.type! === 't') {
        this.tests = res as EcgTests
        this.selectedGroupName = lakeStore.testGroups[gid].groupName
        this.tests.forEach((test) => (this.checkedTestIds[test.id] = false))
      } else {
        this.samples = res as [EcgTest.Meta, number[]][]
        this.selectedGroupName = lakeStore.sampleGroups[gid].groupName
        this.samples.forEach(([test, pages]) => {
          this.checkedTestIds[test.id] = {}
          pages.forEach(
            (p) => ((this.checkedTestIds[test.id] as PageChecked)[p] = false)
          )
        })
      }
      this.loading = false
    },

    async addGroup(groupName: string, groupStatus?: GroupStatus, path = './') {
      this.loading = true
      const res = await api.postAddGroup(
        this.type!,
        groupName,
        groupStatus,
        path
      )
      if (res) {
        const lakeStore = useDataLakeStore()
        await lakeStore.fetchGroupList(this.type!)
      }
      this.loading = false
    },

    async delGroup(gid: number) {
      this.loading = true
      const res = await api.postDelGroup(this.type!, gid)
      if (res) {
        const lakeStore = useDataLakeStore()
        await lakeStore.fetchGroupList(this.type!)
      }
      this.loading = false
    }
  }
})

export default useGroupPageStore
