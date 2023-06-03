import boto3


voiceIds = {
    'Female': {
        'Child': ['Ivy'],
        'Adult': ['Joanna', 'Kendra', 'Kimberly', 'Salli', 'Ruth']
    },
    'Male': {
        'Child': ['Justin', 'Kevin'],
        'Adult': ['Joey', 'Matthew', 'Stephen']
    }
}


def synthesize_speech(text, voiceId, filename):
    polly_client = boto3.Session(
        region_name='us-west-2').client('polly')

    response = polly_client.synthesize_speech(VoiceId=voiceId,
                                              OutputFormat='mp3',
                                              Text=text)

    file = open(filename, 'wb')
    file.write(response['AudioStream'].read())
    file.close()
