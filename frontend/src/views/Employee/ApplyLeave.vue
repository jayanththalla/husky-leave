<template>
  <div class="max-w-xl mx-auto py-8">
    <div class="card space-y-8">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Request Leave</h1>
        <p class="text-gray-600">Submit your application for review</p>
      </div>

      <div v-if="leavesStore.error" class="p-4 bg-red-100 border border-red-200 text-red-700 rounded-md text-sm">
        {{ leavesStore.error }}
      </div>

      <div v-if="successMessage" class="p-4 bg-green-100 border border-green-200 text-green-700 rounded-md text-sm">
        {{ successMessage }}
      </div>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div>
          <label class="label">Leave Category</label>
          <div class="grid grid-cols-3 gap-3">
            <button
              v-for="type in ['sick', 'casual', 'annual']"
              :key="type"
              type="button"
              @click="form.leave_type = type"
              :class="[
                'py-2 px-4 rounded-md border text-sm font-semibold capitalize transition-all',
                form.leave_type === type
                  ? 'bg-blue-600 border-blue-600 text-white shadow-sm'
                  : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
              ]"
            >
              {{ type }}
            </button>
          </div>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div>
            <label class="label">Start Date</label>
            <input v-model="form.start_date" type="date" required class="input-field" />
          </div>

          <div>
            <label class="label">End Date</label>
            <input v-model="form.end_date" type="date" required class="input-field" />
          </div>
        </div>

        <div>
          <label class="label">Total Days</label>
          <input
            v-model.number="form.number_of_days"
            type="number"
            min="1"
            required
            class="input-field"
            placeholder="Duration in days"
          />
        </div>

        <div>
          <label class="label">Reason for Absence</label>
          <textarea
            v-model="form.reason"
            required
            rows="4"
            class="input-field resize-none"
            placeholder="Briefly explain your request..."
          ></textarea>
        </div>

        <div class="flex flex-col sm:flex-row gap-3 pt-4 border-t border-gray-100">
          <button
            type="submit"
            :disabled="leavesStore.loading || !form.leave_type"
            class="btn btn-primary flex-1"
          >
            {{ leavesStore.loading ? 'Submitting...' : 'Submit Request' }}
          </button>
          <router-link
            to="/employee/dashboard"
            class="btn btn-secondary text-center"
          >
            Cancel
          </router-link>
        </div>
      </form>
    </div>
  </div>
</template>


<script setup>
import { ref, reactive } from 'vue'
import { useLeavesStore } from '@/stores/leavesStore'
import { useRouter } from 'vue-router'

const leavesStore = useLeavesStore()
const router = useRouter()
const successMessage = ref('')

const form = reactive({
  leave_type: '',
  start_date: '',
  end_date: '',
  number_of_days: null,
  reason: '',
})

async function handleSubmit() {
  try {
    await leavesStore.createLeaveRequest(form)
    successMessage.value = 'Leave request submitted successfully!'
    
    setTimeout(() => {
      router.push('/employee/dashboard')
    }, 1500)
  } catch (error) {
    // Error is handled by leavesStore
  }
}
</script>
