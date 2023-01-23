// init jspsych and set up prolific
const jsPsych = initJsPsych({
      on_finish: function () {
        window.location = "https://app.prolific.co/submissions/complete?cc=CYD2OXD2"
    },
    show_progress_bar: true,
    auto_update_progress_bar: false
});

const subject_id = jsPsych.data.getURLVariable('PROLIFIC_PID');
const study_id = jsPsych.data.getURLVariable('STUDY_ID');
const session_id = jsPsych.data.getURLVariable('SESSION_ID');
jsPsych.data.addProperties({
    subject_id: subject_id,
    study_id: study_id,
    session_id: session_id
});

// init timeline
var timeline = [];

// preload all images
const preload = {
  type: jsPsychPreload,
  images: [
    'img/jack_has_at_least_average_strength_for_a_beginner_player.png',
    'img/jack_has_at_least_average_strength_for_an_intermediate_player.png',
    'img/jack_has_at_least_average_strength_for_a_professional_player.png',
    'img/jack_is_very_strong_for_a_beginner_player.png',
    'img/jack_is_very_strong_for_an_intermediate_player.png',
    'img/jack_is_very_strong_for_a_professional_player.png',
    'img/jack_has_at_least_average_strength_for_a_novice_player.png',
    'img/jack_has_at_least_average_strength_for_a_mid-level_player.png',
    'img/jack_has_at_least_average_strength_for_an_expert_player.png',
    'img/jack_is_very_strong_for_a_novice_player.png',
    'img/jack_is_very_strong_for_a_mid-level_player.png',
    'img/jack_is_very_strong_for_an_expert_player.png',
    'img/jack_has_at_least_average_strength_for_someone_new_to_the_game.png',
    'img/jack_has_at_least_average_strength_for_someone_with_a_bit_of_experience.png',
    'img/jack_has_at_least_average_strength_for_someone_with_many_years_of_experience.png',
    'img/jack_is_very_strong_for_someone_new_to_the_game.png',
    'img/jack_is_very_strong_for_someone_with_a_bit_of_experience.png',
    'img/jack_is_very_strong_for_someone_with_many_years_of_experience.png',
    'img/jack_is_strong_for_a_beginner_player.png',
  ]
};
timeline.push(preload)

// general instructions
const general_instructions = {
  type: jsPsychInstructions,
  pages: [
  `
  <p>Welcome!</p><p>We are conducting an experiment about word meanings. Your answers will be used
  to inform computer science and cognitive science research about language processing.</p>
  <p>This experiment should take at most <b>10 minutes</b>. You will be compensated at a base rate 
  of $15.00/hour for a total of <b>$2.50</b>, which you will receive as long as you complete the study.</p>
  <p>We take your compensation and time seriously! The email for the main experimenter is <b>lipkinb@mit.edu</b>. 
  Please write this down now, and email us with your Prolific ID and the subject line "Prolific Experiment" 
  if you have problems submitting this task, or if it takes much more time than expected.</p>
  <p>This experiment must be completed in <b>full-screen</b> in order to view all the required components. 
  Please make sure you are set up, and then press <b>"Next"</b> when ready to read the task instructions.</p>
  `
  ],
  show_clickable_nav: true
};
timeline.push(general_instructions)

// task instruction loop
const task_instructions = {
  type: jsPsychInstructions,
  pages: [
  `
  <p>In this experiment, you will be reading <b>sentences describing a fictional athlete named Jack, 
  who plays in a tug-of-war league.</b></p>
  <p>For each sentence, your task is to <b>move a slider indicating how <em>strong</em> you think Jack is, 
  based on the particular sentence that you just read.</b></p>
  <br>
  <p>Press Next to read more about this experiment.</p>
  `,
  `
  <p>You will read sentences one at a time, on a screen like the example below.</p>
  <p>These sentences will describe <b>how strong Jack is.</b></p>
  <p>As you can see from the screen, strength is measured on a scale from 0 to 100.</p>
  <br>
  <img src="img/jack_is_strong_for_a_beginner_player.png" height="450" width="600" style="border:5px solid #000000; padding:25px">
  `,
  `
  <and>In this world, there are three different leagues of players: 
  <em>"Beginners"</em>, <em>"Intermediates"</em>, and <em>"Professionals"</em>,
  and each league is defined by their typical strength.
  <b>Beginners have an average strength of 30</b>, <b>intermediates have an average strength of 50</b>, 
  and <b>professionals have an average strength of 70</b>, but there is some variability and crossover.</p>
  <p>Your task is to <b>read each sentence</b> and then <b>move the slider to show how strong you think Jack is</b>, 
  based on that sentence only.</p>
  <br>
  <img src="img/jack_is_strong_for_a_beginner_player.png" height="450" width="600" style="border:5px solid #000000; padding:25px">
  <br>
  `,
  `
  <p>For instance, in this example, based on the sentence "<b><em>Jack is strong for a beginner player</em></b>", 
  this participant has moved the slider to indicate that they think that <b>Jack's minimum strength is at least 40</b>,
  incorporating hints about both Jack's league as well as his relative strength within the league.
  This means that Jack is <em>at least as strong as 40</em> on this scale, 
  but <em>not any weaker</em>.</p>
  <p>When ready, press next to complete a quick comprehension check, and then proceed to the experiment.</p>
  <br>
  <img src="img/jack_is_strong_for_a_beginner_player.png" height="450" width="600" style="border:5px solid #000000; padding:25px">
  <br>
  `
],
  show_clickable_nav: true
};

const task_comprehension_check = {
    type: jsPsychSurveyMultiChoice,
    preamble: [`
      <p>Check your knowledge before you begin. If you don't know the answers, 
      don't worry; we will show you the instructions again.</p>
    `],
    questions: [
        {
            prompt: "What will you be doing in this task?",
            options: [
              "Reading sentences about a fictional athlete named Jack.",
              "Looking at pictures of a fictional athlete named Jack.",
              "Writing a description of a fictional athlete named Jack."
            ],
            required: true
        }, {
            prompt: "You will be reading questions about how strong Jack is, and moving the slider to indicate:",
            options: [
              "Jack's <em>minimum</em> strength.",
              "Jack's <em>maximum</em> strength"
            ],
            required: true
        }, {
            prompt: "On the numeric scale we use to show strength, what is the average strength for a professional?",
            options: [
              "0",
              "30",
              "50",
              "70",
              "100"
            ],
            required: true
        }
    ],
    on_finish: function (data) {
        var responses = data.response;
        if ( responses['Q0'] == "Reading sentences about a fictional athlete named Jack."
          && responses['Q1'] == "Jack's <em>minimum</em> strength."
          && responses['Q2'] == "70"
          ) {
            correct = true;
        } else {
            correct = false;
        }
    }
}

const task_instruction_timeline = [task_instructions, task_comprehension_check]
const task_instruction_loop = {
    timeline: task_instruction_timeline,
    loop_function: function (data) {
        return !correct;
    }
}
timeline.push(task_instruction_loop)

const final_instructions = {
  type: jsPsychInstructions,
  pages: [
  `
  <p>You are now about to begin the experiment.</p>
  <p>There will be 18 trials.</p>
  <p>Remember, you will move the slider to indicate your estimate of Jack's <b>minimum</b> strength, based on the hint.</p>
  <p>The hint will include both information about Jack's league, either explicitly or by allusion, and his relative strength within that league.</p>
  <p>As a reminder, you should read <b>each sentence separately</b>, 
  and move each slider to indicate how strong Jack is <b>based only on that sentence.</b></p>
  <p>Please click <b>"Next"</b> to start the experiment.</p>
  `
  ],
  show_clickable_nav: true
};
timeline.push(final_instructions)

// trials
const trial_prompt = "<p><em>(Interaction with slider is required).</em></p>"

const trial_stimuli = [
  { stimulus: 'img/jack_has_at_least_average_strength_for_a_beginner_player.png' },
  { stimulus: 'img/jack_has_at_least_average_strength_for_an_intermediate_player.png' },
  { stimulus: 'img/jack_has_at_least_average_strength_for_a_professional_player.png' },
  { stimulus: 'img/jack_is_very_strong_for_a_beginner_player.png' },
  { stimulus: 'img/jack_is_very_strong_for_an_intermediate_player.png' },
  { stimulus: 'img/jack_is_very_strong_for_a_professional_player.png' },
  { stimulus: 'img/jack_has_at_least_average_strength_for_a_novice_player.png' },
  { stimulus: 'img/jack_has_at_least_average_strength_for_a_mid-level_player.png' },
  { stimulus: 'img/jack_has_at_least_average_strength_for_an_expert_player.png' },
  { stimulus: 'img/jack_is_very_strong_for_a_novice_player.png' },
  { stimulus: 'img/jack_is_very_strong_for_a_mid-level_player.png' },
  { stimulus: 'img/jack_is_very_strong_for_an_expert_player.png' },
  { stimulus: 'img/jack_has_at_least_average_strength_for_someone_new_to_the_game.png' },
  { stimulus: 'img/jack_has_at_least_average_strength_for_someone_with_a_bit_of_experience.png' },
  { stimulus: 'img/jack_has_at_least_average_strength_for_someone_with_many_years_of_experience.png' },
  { stimulus: 'img/jack_is_very_strong_for_someone_new_to_the_game.png' },
  { stimulus: 'img/jack_is_very_strong_for_someone_with_a_bit_of_experience.png' },
  { stimulus: 'img/jack_is_very_strong_for_someone_with_many_years_of_experience.png' },
];

const trial = {
  type: jsPsychImageSliderResponse,
  stimulus: jsPsych.timelineVariable('stimulus'),
  prompt: trial_prompt,
  stimulus_width: 600, slider_width: 550,
  min: 0, max: 100, step: 10, slider_start: 0,
  labels: ['0','10','20','30','40','50','60','70','80','90','100'],
  require_movement: true,
  on_finish: function () {
    jsPsych.setProgressBar(jsPsych.getProgressBarCompleted() + 1/18);
  }
};

const trials = {
  timeline: [trial],
  timeline_variables: trial_stimuli,
  repetitions: 1,
  randomize_order: true
};
timeline.push(trials)

// wrap up
const comments_block = {
    type: jsPsychSurveyText,
    preamble: `
      <p>Thank you for participating in our study!</p>
      <p>Click <b>"Finish"</b> to complete the experiment and receive 
      compensation. If you have any comments about the experiment, please let 
      us know in the form below.</p>`,
    questions: [
      {prompt: "Were the instructions clear? (On a scale of 1-10, with 10 being very clear)"},
      {prompt: "How challenging was it to determine the strength thresholds? (On a scale of 1-10, with 10 being very challenging)"},
      {prompt: "Did you get bored during the task? (Yes, No, or Sort of)"},
      {prompt: "Do you have any additional comments to share with us?",rows: 5, columns: 50}],
    button_label: "Finish",
};
timeline.push(comments_block)

// run timeline
jsPsych.run(timeline);
