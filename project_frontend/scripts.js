function display_user_test_configurations(event)
        {
            event.preventDefault(); // Prevent the form from submitting normally
            
            var email = document.getElementById('email').value;
            var password = document.getElementById('password').value;

            fetch('http://127.0.0.1:5000/user', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    user_email: email, 
                    user_password: password 
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.message == "Successful") {
                    // Hide sign-in-section and show tests section
                    document.getElementById('sign-in-section').classList.add('hidden');
                    document.getElementById('test-section').classList.remove('hidden');

                    var user_id = data.user_id;
                    data.test_configs.forEach(config => {
                        document.getElementById('test-section').innerHTML += 
                        `<div class="tests" id="tests">
                            <div class="test-name">${config.subject_name}</div><br>
                            <div class="test-no-of-questions">Total number of questions: ${config.no_of_questions}</div>
                            <div class="test-mark">Total marks: ${config.marks}</div>
                            <div class="test-cutoff">Cut-off marks: ${config.cut_off}</div>
                            <div class="test-duration">Duration: ${config.test_duration}</div>
                            <div class="take-test-button"><button onclick="display_mcq_test(event, ${user_id}, ${config.threshold}, ${config.subject_id}, ${config.marks}, ${config.no_of_questions}, ${config.cut_off}, '${config.test_duration}')">Take Test</button></div>
                        </div>`;
                    });
                } 
                else {
                    document.getElementById('message').innerHTML = '<div>' + data.message + '</div>';
                }
            })
            .catch(error => console.error('Error:', error));
        }

        function display_mcq_test(event, user_id, threshold, subject_id, marks, no_of_questions, cut_off, test_duration)
        {
            event.preventDefault();

            fetch('http://127.0.0.1:5000/test', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    user_id: user_id,
                    threshold: threshold,
                    subject_id: subject_id,
                    marks: marks,
                    no_of_questions: no_of_questions,
                    cut_off: cut_off,
                    test_duration: test_duration
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                document.getElementById('test-section').classList.add('hidden');
                document.getElementById('mcq-section').classList.remove('hidden');

                var test_id = data.test_id;
                var count = 1;
                console.log(data.mcq_questions)
                data.mcq_questions.forEach(q => {
                    var q_name = "question" + count;
                    var option_1 = q.option_1;
                    var option_2 = q.option_2;
                    var option_3 = q.option_3;
                    var option_4 = q.option_4;
                    document.getElementById('mcq-section').innerHTML +=
                    `<div class="question-box">
                        <form class="each-question">
                            <label for=${q_name}>${count}) ${q.question}</label><br>
                            <input name=${q_name} type="radio" value="${option_1}">${option_1}<br>
                            <input name=${q_name} type="radio" value="${option_2}">${option_2}<br>
                            <input name=${q_name} type="radio" value="${option_3}">${option_3}<br>
                            <input name=${q_name} type="radio" value="${option_4}">${option_4}<br>
                        </form>
                    </div>`;
                    count += 1;
                });
                document.getElementById('mcq-section').innerHTML += `<button onclick="display_result(event,${count},${test_id})">Submit</button>`;
            })
            .catch(error => console.error('Error:', error));
        }

        function display_result(event, count, test_id)
        {
            event.preventDefault();
            var answer_list=[];
            for(let i=1;i<=count;i++)
            {
                q_name="question"+i;
                var options=document.getElementsByName(q_name);
                for(let j=0;j<options.length;j++)
                {
                    if(options[j].checked)
                    {
                        answer_list.push(options[j].value);
                    }
                }
            }
            fetch('http://127.0.0.1:5000/result', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ 
                    test_id: test_id,
                    answer_list: answer_list
                })
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                document.getElementById('mcq-section').classList.add('hidden');
                document.getElementById('result-section').classList.remove('hidden');
                var marks=data.marks;
                var cut_off=data.cut_off;
                var result;
                if(marks>=cut_off){
                    result="Pass";
                }
                else{
                    result="Fail";
                }
                document.getElementById("result-section").innerHTML+=
                `<div class="result-box">
                    <div>Marks:${marks}</div>
                    <div>Result:${result}</div>
                </div>`;
            })
            .catch(error => console.error('Error:', error));
        }