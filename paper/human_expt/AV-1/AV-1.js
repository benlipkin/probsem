// init jspsych and set up prolific
const jsPsych = initJsPsych({
      on_finish: function () {
        window.location = ""
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
    'img/jack_is_super_strong.png',
    'img/jack_is_a_bit_weak.png',
    'img/jack_has_at_least_average_strength.png',
    'img/jack_has_at_most_average_strength.png',
    'img/jack_is_not_so_strong.png',
    'img/jack_is_not_so_weak.png',
    'img/jack_is_not_strong.png',
    'img/jack_is_not_that_strong.png',
    'img/jack_is_not_that_weak.png',
    'img/jack_is_not_very_strong.png',
    'img/jack_is_not_very_weak.png',
    'img/jack_is_not_weak.png',
    'img/jack_is_pretty_strong.png',
    'img/jack_is_pretty_weak.png',
    'img/jack_is_somewhat_strong.png',
    'img/jack_is_somewhat_weak.png',
    'img/jack_is_strong.png',
    'img/jack_is_very_strong.png',
    'img/jack_is_very_weak.png',
    'img/jack_is_weak.png',
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
  <p> We take your compensation and time seriously! The email for the main experimenter is <b>lipkinb@mit.edu</b>. 
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
  <p>In this experiment, you will be reading <b>sentences describing a fictional athlete named Jack.</b></p>
  <p>For each sentence, your task is to <b>move a slider indicating how <em>strong</em> or how 
  <em>weak</em> you think Jack is, based on the particular sentence that you just read.</b></p>
  <br>
  <p>This experiment will have <b>two parts</b>. Press Next to read about the first part of this experiment.</p>
  `,
  `
  <p>In Part One of this experiment, you will read sentences one at a time, on a screen like the example below.</p>
  <p>These sentences will describe <b>how strong Jack is.</b></p>
  <br>
  <p>As you can see from the screen, strength is measured on a scale from 0 to 100, with <b>50 being the average.</b></p>
  <p>Your task is to <b>read each sentence</b> and then <b>move the slider to show how strong you think Jack is</b>, 
  based on that sentence only.</p>
  <p>In this section, the slider indicates <b><span style="color: #1f77b4">Jack's minimum strength.</span></b></p>
  <br>
  <img src="img/jack_is_super_strong.png" height="400" width="600" style="border:5px solid #000000; padding:25px">
  <br>
  `,
  `
  <p>For instance, in this example, based on the sentence "<b><em>Jack is super strong</em></b>", 
  this participant has moved the slider to indicate that they think that based on the description, 
  <b>Jack's minimum strength is at least 80</b>. This means that Jack is <em>at least as strong as 80</em> on this scale, 
  but <em>not any weaker</em>.</p>
  <br>
  <p>When ready, press next to complete a quick comprehension check, and then proceed to Part One.</p>
  <br>
  <img src="img/jack_is_super_strong.png" height="400" width="600" style="border:5px solid #000000; padding:25px">
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
            prompt: "In Part One, you will be reading questions about how strong Jack is, and moving the slider to indicate:",
            options: [
              "Jack's <em>minimum</em> strength.",
              "Jack's <em>maximum</em> strength"
            ],
            required: true
        }, {
            prompt: "On the numeric scale we use to show strength, what is the average strength?",
            options: [
              "0",
              "50",
              "100"
            ],
            required: true
        }
    ],
    on_finish: function (data) {
        var responses = data.response;
        if ( responses['Q0'] == "Reading sentences about a fictional athlete named Jack."
          && responses['Q1'] == "Jack's <em>minimum</em> strength."
          && responses['Q2'] == "50"
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

const final_strong_instructions = {
  type: jsPsychInstructions,
  pages: [
  `
  <p>You are now about to begin part 1 of 2.</p>
  <p>There will be 9 trials in this section.</p>
  <p>Remember, you will move the slider to indicate your estimate of Jack's <b>minimum</b> strength, based on the hint.</p>
  <p>As a reminder, you should read <b>each sentence separately</b>, 
  and move each slider to indicate how strong Jack is <b>only based on that sentence.</b></p>
  <p>Please click <b>"Next"</b> to start the experiment.</p>
  `
  ],
  show_clickable_nav: true
};
timeline.push(final_strong_instructions)

// strong trials
const trial_prompt = "<p><em>(Interaction with slider is required).</em></p>"

const strong_trial_stimuli = [
  { stimulus: "img/jack_is_strong.png" },
  { stimulus: "img/jack_is_very_strong.png" },
  { stimulus: "img/jack_is_somewhat_strong.png" },
  { stimulus: "img/jack_is_pretty_strong.png" },
  { stimulus: "img/jack_has_at_least_average_strength.png" },
  { stimulus: "img/jack_is_not_weak.png" },
  { stimulus: "img/jack_is_not_so_weak.png" },
  { stimulus: "img/jack_is_not_that_weak.png" },
  { stimulus: "img/jack_is_not_very_weak.png" },
];

const strong_trial = {
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

const strong_trials = {
  timeline: [strong_trial],
  timeline_variables: strong_trial_stimuli,
  repetitions: 1,
  randomize_order: true
};
timeline.push(strong_trials)

// weak instruction loop
const weak_instructions = {
  type: jsPsychInstructions,
  pages: [
  `
  <p>Great job! You are now moving on to Part Two of the experiment.</p>
  <p>In Part Two, you will again be reading sentences one at a time, on a screen like the example below.</p>
  <br>
  <p>This time, the sentences will describe <b>how weak Jack is.</b></p>
  <p>As with before, strength is measured on a scale from 0 to 100, with <b>50 being the average.</b></p>
  <p>However, your task is now to <b>read each sentence</b> and then 
  <b>move the slider to show how <em>weak</em> you think Jack is</b>, based on that sentence only.</p>
  <p>In this section, the slider now indicates <b><span style="color: #d62728">Jack's maximum strength.</span></b></p>
  <br>
  <img src="img/jack_is_a_bit_weak.png" height="400" width="600" style="border:5px solid #000000; padding:25px">
  <br>
  `,
  `
  <p>For instance, in this example, based on the sentence "<b><em>Jack is a bit weak</em></b>", 
  this participant has moved the slider to indicate that they think that based on the description, 
  <b>Jack's maximum strength is at most 40</b>. This means that Jack is <em>at most as strong as 40</em> on this scale, 
  but <em>not any stronger than that.</em></p>
  <br>
  <p>When ready, press next to complete a quick comprehension check, and then proceed to Part Two.</p>
  <br>
  <img src="img/jack_is_a_bit_weak.png" height="400" width="600" style="border:5px solid #000000; padding:25px">
  <br>
  `
  ],
  show_clickable_nav: true
};

const weak_comprehension_check = {
    type: jsPsychSurveyMultiChoice,
    preamble: [`
      <p>Check your knowledge before you begin. If you don't know the answers, 
      don't worry; we will show you the instructions again.</p>
    `],
    questions: [
        {
            prompt: "In Part Two, you will be reading questions about how weak Jack is, and moving the slider to indicate:",
            options: [
              "Jack's <em>minimum</em> strength.",
              "Jack's <em>maximum</em> strength."
            ],
            required: true
        }
    ],
    on_finish: function (data) {
        var responses = data.response;
        if ( responses['Q0'] == "Jack's <em>maximum</em> strength."
          ) {
            correct = true;
        } else {
            correct = false;
        }
    }
}

const weak_instruction_timeline = [weak_instructions, weak_comprehension_check]
const weak_instruction_loop = {
    timeline: weak_instruction_timeline,
    loop_function: function (data) {
        return !correct;
    }
}
timeline.push(weak_instruction_loop)

const final_weak_instructions = {
  type: jsPsychInstructions,
  pages: [`
  <p>You are now about to begin part 2 of 2.</p>
  <p>There will be 9 trials in this section.</p>
  <p>Remember, you will move the slider to indicate your estimate of Jack's <b>maximum</b> strength, based on the hint.</p>
  <p>As a reminder, you should read <b>each sentence separately</b>, 
  and move each slider to indicate how strong Jack is <b>only based on that sentence.</b></p>
  <p>Please click <b>"Next"</b> to start the experiment.</p>
  `],
  show_clickable_nav: true
};
timeline.push(final_weak_instructions)

// weak trials
const weak_trial_stimuli = [
  { stimulus: "img/jack_is_weak.png" },
  { stimulus: "img/jack_is_very_weak.png" },
  { stimulus: "img/jack_is_somewhat_weak.png" },
  { stimulus: "img/jack_is_pretty_weak.png" },
  { stimulus: "img/jack_has_at_most_average_strength.png" },
  { stimulus: "img/jack_is_not_strong.png" },
  { stimulus: "img/jack_is_not_so_strong.png" },
  { stimulus: "img/jack_is_not_that_strong.png" },
  { stimulus: "img/jack_is_not_very_strong.png" }
];

const weak_trial = {
  type: jsPsychImageSliderResponse,
  stimulus: jsPsych.timelineVariable('stimulus'),
  prompt: trial_prompt,
  stimulus_width: 600, slider_width: 550,
  min: 0, max: 100, step: 10, slider_start: 100,
  labels: ['0','10','20','30','40','50','60','70','80','90','100'],
  require_movement: true,
  on_finish: function () {
    jsPsych.setProgressBar(jsPsych.getProgressBarCompleted() + 1/18);
  }
};

const weak_trials = {
  timeline: [weak_trial],
  timeline_variables: weak_trial_stimuli,
  repetitions: 1,
  randomize_order: true
};
timeline.push(weak_trials)

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
