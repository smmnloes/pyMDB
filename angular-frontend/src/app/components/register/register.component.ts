import {Component, OnInit} from '@angular/core';
import {AuthService} from "../../services/auth.service";
import {FormBuilder, FormGroup} from "@angular/forms";
import {ToastrService} from "ngx-toastr";

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  registerData: FormGroup;

  constructor(private authService: AuthService, private formBuilder: FormBuilder, private toastrService: ToastrService) {
    this.registerData = formBuilder.group(
      {
        email: '',
        password: '',
        username: ''
      }
    )
  }

  ngOnInit(): void {
  }

  onSubmit(registerData) {
    this.authService.register(registerData.email, registerData.password, registerData.username);
  }

  onSuccessfulRegistration(userData): void {

  }

}
