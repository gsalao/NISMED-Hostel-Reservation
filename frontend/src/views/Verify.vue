<script setup>
  import { ref, onMounted } from 'vue'
  import { useRoute } from 'vue-router'

  const route = useRoute()
  const token = ref(route.query.token || '')
  const code = ref('')
  const verified = ref(false)
  const error = ref('')

  const verify = async () => {
    error.value = ''
    if (!token.value || !code.value) {
      error.value = "Missing token or code."
      return
    }

    try {
      const res = await fetch('http://127.0.0.1:8000/api/reserve/verify_reservation/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ reservation_token: token.value, code: code.value })
      })

      const result = await res.json()
      if (res.ok && result.success) {
        verified.value = true
      } else {
        error.value = result.error || "Verification failed"
      }
    } catch (err) {
      error.value = "Network error: " + err.message
    }
  }
</script>

<template>
  <div class="max-w-xl mx-auto mt-20 p-6 border rounded shadow bg-white">
    <h2 class="text-2xl font-bold mb-4 text-center">Reservation Verification</h2>
    <p class="mb-4 text-justify">Please enter the 6-digit code sent to your email to verify your reservation. A <strong>confirmation message</strong> will be sent to the email you registered.</p>

    <input
      v-model="code"
      maxlength="6"
      class="w-full p-2 border mb-4"
      placeholder="Enter verification code"
    />

    <button
      @click="verify"
      class="cursor-pointer w-full bg-green-800 text-white py-2 rounded hover:bg-green-700"
    >
      Verify Reservation
    </button>

    <p v-if="verified" class="mt-4 text-green-600 font-semibold">Reservation successfully verified!</p>
    <p v-if="error" class="mt-4 text-red-600">{{ error }}</p>
  </div>
</template>