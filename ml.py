import numpy as np
from sklearn.ensemble import IsolationForest

def detect_third_party(exchanged_data):
    # Prepare the data for the model
    data = np.array(exchanged_data).reshape(-1, 1)

    # Create and train the Isolation Forest model
    model = IsolationForest(contamination='auto', random_state=42)
    model.fit(data)

    # Predict the anomaly scores for the data
    anomaly_scores = -model.decision_function(data)

    # Determine if there is a third party based on anomaly scores
    is_third_party = any(score < 0 for score in anomaly_scores)

    return is_third_party


# Example usage with a larger dataset
if __name__ == '__main__':
    # Simulating the Diffie-Hellman key exchange
    alice_private_key = 12345
    bob_private_key = 67890
    prime_number = 65537
    shared_base = 3

    # Generate a larger dataset of exchanged data
    num_exchanges = 10
    exchanged_data = []

    for _ in range(num_exchanges):
        # Alice's step
        alice_partial_key = pow(shared_base, alice_private_key, prime_number)

        # Bob's step
        bob_partial_key = pow(shared_base, bob_private_key, prime_number)

        # Interchanged data
        exchanged_data.append(alice_partial_key)
        exchanged_data.append(bob_partial_key)

    # Injecting a third party
    third_party_partial_key = pow(shared_base, 98765, prime_number)
    exchanged_data.append(third_party_partial_key)

    # Detecting third party
    is_third_party_detected = detect_third_party(exchanged_data)

    if is_third_party_detected:
        print("Potential third party detected in the Diffie-Hellman key exchange!")
    else:
        print("No third party detected in the Diffie-Hellman key exchange!")
