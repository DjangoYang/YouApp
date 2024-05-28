import os
import zipfile

# Define directory structure
directories = [
    "youapp/flutter/lib/bloc",
    "youapp/flutter/lib/models",
    "youapp/flutter/lib/ui",
    "youapp/flutter/lib/services",
    "youapp/nextjs/components",
    "youapp/nextjs/services",
    "youapp-backend/src/auth",
    "youapp-backend/src/chat",
    "youapp-backend/src/schemas",
    "youapp-backend/src/users"
]

# Define files and their content
files = {
    "youapp/flutter/pubspec.yaml": """
name: youapp
description: A new Flutter project.

dependencies:
  flutter:
    sdk: flutter
  flutter_bloc: ^7.0.0
  http: ^0.13.3
""",
    "youapp/flutter/lib/bloc/authentication_bloc.dart": """
import 'package:bloc/bloc.dart';

enum AuthenticationEvent { login, logout }

class AuthenticationBloc extends Bloc<AuthenticationEvent, bool> {
  AuthenticationBloc() : super(false);

  @override
  Stream<bool> mapEventToState(AuthenticationEvent event) async* {
    if (event == AuthenticationEvent.login) {
      yield true;
    } else if (event == AuthenticationEvent.logout) {
      yield false;
    }
  }
}
""",
    "youapp/flutter/lib/services/api_service.dart": """
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl = 'http://techtest.youapp.ai/api';

  Future<http.Response> login(String username, String password) {
    return http.post(
      Uri.parse('$baseUrl/login'),
      body: {'username': username, 'password': password},
    );
  }

  // Implement other API calls similarly
}
""",
    "youapp/nextjs/package.json": """
{
  "name": "youapp",
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "latest",
    "react": "latest",
    "react-dom": "latest",
    "tailwindcss": "^2.2.19"
  }
}
""",
    "youapp/nextjs/services/apiService.js": """
export const login = async (username, password) => {
  const response = await fetch('http://techtest.youapp.ai/api/login', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, password }),
  });
  return response.json();
};
""",
    "youapp-backend/package.json": """
{
  "name": "youapp-backend",
  "version": "1.0.0",
  "scripts": {
    "start": "nest start"
  },
  "dependencies": {
    "@nestjs/common": "^7.6.15",
    "@nestjs/core": "^7.6.15",
    "@nestjs/jwt": "^7.0.0",
    "@nestjs/mongoose": "^7.2.4",
    "@nestjs/passport": "^7.1.5",
    "@nestjs/platform-express": "^7.6.15",
    "@nestjs/websockets": "^7.6.15",
    "mongoose": "^5.12.14",
    "passport-jwt": "^4.0.0",
    "socket.io": "^4.1.2"
  }
}
""",
    "youapp-backend/src/main.ts": """
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  await app.listen(3000);
}
bootstrap();
""",
    "youapp-backend/src/app.module.ts": """
import { Module } from '@nestjs/common';
import { AuthModule } from './auth/auth.module';
import { UsersModule } from './users/users.module';
import { MongooseModule } from '@nestjs/mongoose';
import { ChatModule } from './chat/chat.module';

@Module({
  imports: [
    MongooseModule.forRoot('mongodb://localhost/nest'),
    AuthModule,
    UsersModule,
    ChatModule,
  ],
})
export class AppModule {}
""",
    "youapp-backend/src/auth/auth.module.ts": """
import { Module } from '@nestjs/common';
import { JwtModule } from '@nestjs/jwt';
import { PassportModule } from '@nestjs/passport';
import { AuthService } from './auth.service';
import { JwtStrategy } from './jwt.strategy';
import { UsersModule } from '../users/users.module';

@Module({
  imports: [
    UsersModule,
    PassportModule,
    JwtModule.register({
      secret: 'SECRET_KEY',
      signOptions: { expiresIn: '60s' },
    }),
  ],
  providers: [AuthService, JwtStrategy],
  exports: [AuthService],
})
export class AuthModule {}
""",
    "youapp-backend/src/auth/auth.service.ts": """
import { Injectable } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';

@Injectable()
export class AuthService {
  constructor(private readonly jwtService: JwtService) {}

  async login(user: any) {
    const payload = { username: user.username, sub: user.userId };
    return {
      access_token: this.jwtService.sign(payload),
    };
  }

  // Other methods for registration and validation
}
""",
    "youapp-backend/src/auth/jwt.strategy.ts": """
import { Strategy } from 'passport-jwt';
import { PassportStrategy } from '@nestjs/passport';
import { Injectable } from '@nestjs/common';
import { ExtractJwt } from 'passport-jwt';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor() {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: 'SECRET_KEY',
    });
  }

  async validate(payload: any) {
    return { userId: payload.sub, username: payload.username };
  }
}
"""
}

# Create directories
for directory in directories:
    os.makedirs(directory, exist_ok=True)

# Create files with content
for file_path, content in files.items():
    with open(file_path, 'w') as file:
        file.write(content)

# Zip the created directory
zipf = zipfile.ZipFile('youapp_project.zip', 'w', zipfile.ZIP_DEFLATED)
for root, dirs, files in os.walk('youapp'):
    for file in files:
        zipf.write(os.path.join(root, file))
for root, dirs, files in os.walk('youapp-backend'):
    for file in files:
        zipf.write(os.path.join(root, file))
zipf.close()

print("Project structure created and zipped successfully.")
