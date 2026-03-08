import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import client from '@/api/client'

export const useLeavesStore = defineStore('leaves', () => {
  const leaves = ref([])
  const loading = ref(false)
  const error = ref(null)
  const filterStatus = ref(null)

  const filteredLeaves = computed(() => {
    if (!filterStatus.value) return leaves.value
    return leaves.value.filter((leave) => leave.status === filterStatus.value)
  })

  const pendingCount = computed(() => leaves.value.filter((l) => l.status === 'pending').length)
  const approvedCount = computed(() => leaves.value.filter((l) => l.status === 'approved').length)
  const rejectedCount = computed(() => leaves.value.filter((l) => l.status === 'rejected').length)

  async function fetchMyLeaves() {
    loading.value = true
    error.value = null
    try {
      const response = await client.get('/api/leaves/my-requests')
      leaves.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch leaves'
      console.error('Error fetching leaves:', err)
    } finally {
      loading.value = false
    }
  }

  async function fetchAllLeaves(status = null) {
    loading.value = true
    error.value = null
    try {
      const params = status ? { status } : {}
      const response = await client.get('/api/leaves/all', { params })
      leaves.value = response.data
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to fetch leaves'
      console.error('Error fetching all leaves:', err)
    } finally {
      loading.value = false
    }
  }

  async function createLeaveRequest(leaveData) {
    loading.value = true
    error.value = null
    try {
      const response = await client.post('/api/leaves/request', leaveData)
      leaves.value.unshift(response.data)
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to create leave request'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  async function updateLeaveStatus(requestId, status, remarks = null) {
    loading.value = true
    error.value = null
    try {
      const response = await client.patch(`/api/leaves/${requestId}`, {
        status,
        remarks,
      })
      const index = leaves.value.findIndex((l) => l._id === requestId)
      if (index !== -1) {
        leaves.value[index] = response.data
      }
      return response.data
    } catch (err) {
      error.value = err.response?.data?.detail || 'Failed to update leave status'
      throw error.value
    } finally {
      loading.value = false
    }
  }

  function setFilter(status) {
    filterStatus.value = status
  }

  function clearFilter() {
    filterStatus.value = null
  }

  return {
    leaves,
    loading,
    error,
    filterStatus,
    filteredLeaves,
    pendingCount,
    approvedCount,
    rejectedCount,
    fetchMyLeaves,
    fetchAllLeaves,
    createLeaveRequest,
    updateLeaveStatus,
    setFilter,
    clearFilter,
  }
})
